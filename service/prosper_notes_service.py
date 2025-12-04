import json
import logging
import traceback
from dataclasses import asdict

from model.filterset import *
from service.notification_service import NotificationService
from service.prosper_rest_service import ProsperRestService


class ProsperNotesService:

    def __init__(self, prosper_config):
        self.prosper_config = prosper_config
        self.logger = logging.getLogger(__name__)
        self.prosper_rest_service = ProsperRestService(prosper_config)
        self.notification_service = NotificationService(self.prosper_config)

    def filter_listings(self, listings, max_loan_count):
        filtered_listings = list()
        if listings.result is not None:
            for filter_set in self.prosper_config.filter_set_properties.filter_set_list:
                self.logger.info(f"FilterSet in effect if Loan Count Over: {filter_set.loan_count_over}")
                if filter_set.loan_count_over <= max_loan_count:
                    self.logger.info(f"FilterSet in effect: {filter_set}")
                    for listing in listings.result:
                        if (
                                check_grade(filter_set, listing.prosper_rating)
                                and check_employment_length(filter_set, listing.months_employed)
                                and listing.credit_bureau_values_transunion_indexed is not None
                                and check_inquiries(filter_set, listing.credit_bureau_values_transunion_indexed.g980s_inquiries_in_the_last_6_months)
                                and check_delinquencies(filter_set, listing.credit_bureau_values_transunion_indexed.g218b_number_of_delinquent_accounts)
                                and listing.stated_monthly_income > 0
                                and check_payment_income_ratio(filter_set, listing.listing_monthly_payment, listing.stated_monthly_income)
                        ):
                            filtered_listings.append(listing)
                            self.logger.info(f"Adding Listing: {listing.listing_number}")
                else:
                    self.logger.info(f"FilterSet skipped: {filter_set}")
        return filtered_listings

    def trim_filtered_listing(self, filtered_listings, max_loan_count):
        orders_list = self.prosper_rest_service.get_orders_list()
        trimmed_listings = list(filtered_listings)
        if orders_list is not None and orders_list.result is not None:
            for orders_response in orders_list.result:
                if (
                        orders_response.order_status == "IN_PROGRESS"
                        and orders_response.bid_requests is not None
                ):
                    for bid_request in orders_response.bid_requests:
                        for listing in list(trimmed_listings):
                            if bid_request.listing_id == listing.listing_number:
                                self.logger.info(f"Removing Listing already ordered: {listing.listing_number}")
                                trimmed_listings.remove(listing)
            # Truncate if more than max_loan_count
            if len(trimmed_listings) > max_loan_count:
                self.logger.info(f"Truncating order to max listing count of {max_loan_count}")
                trimmed_listings = list(list(trimmed_listings)[:max_loan_count])
        return trimmed_listings

    def create_order_request(self, listings, max_loan_count):
        orders_request = dict()
        bid_requests = list()
        order_ids = list()
        for i, listing in enumerate(list(listings)[:min(max_loan_count, 100)]):
            if listing.listing_number not in order_ids:
                order_ids.append(listing.listing_number)
                bid_request = {"listing_id": listing.listing_number, "bid_amount": self.prosper_config.minimum_investment_amount}
                bid_requests.append(bid_request)
        orders_request.update({"bid_requests": bid_requests})
        self.logger.info(f"Created OrdersRequest: {orders_request}")
        return orders_request

    def buy_notes(self):
        try:
            # Determine how much cash is available to invest
            self.logger.info("Retrieving account information...")
            account = self.prosper_rest_service.get_account()
            self.logger.debug(f"Account information: {json.dumps(asdict(account), indent=4)}")
            available_cash = account.available_cash_balance
            self.logger.info(f"Available cash balance: {available_cash}")
            if self.prosper_config.run_mode == "test" or available_cash >= self.prosper_config.minimum_investment_amount:
                self.logger.info("Getting listings...")
                listings = self.prosper_rest_service.get_listings()
                self.logger.info(f"Total listings retrieved: {len(listings.result)}")
                if listings.result_count > 0:
                    self.logger.debug(f"Listings: {json.dumps([asdict(listing) for listing in listings.result], indent=4)}")

                    # Find the maximum load count we can invest in by dividing the available cash by the minimum investment amount, rounding down
                    max_loan_count = int(available_cash / self.prosper_config.minimum_investment_amount)
                    self.logger.info(f"Maximum loan count based on available cash: {max_loan_count}")

                    # Filter the listings based on the filter sets
                    self.logger.info("Processing listings...")
                    filtered_listings = self.filter_listings(listings, max_loan_count)
                    if filtered_listings and len(filtered_listings) > 0:
                        self.logger.info(f"Filtered listings count: {len(filtered_listings)}")

                        # Trim the filtered listings based on existing orders
                        trimmed_listings = self.trim_filtered_listing(filtered_listings, max_loan_count)
                        self.logger.info(f"Trimmed listings count: {len(trimmed_listings)}")

                        # If RUN_MODE is prod, create the order request and submit it
                        if trimmed_listings and len(trimmed_listings) > 0 and self.prosper_config.run_mode == "prod":
                            self.logger.info("Proceeding to buy notes...")
                            self.logger.debug(f"Trimmed listings: {json.dumps([asdict(listing) for listing in trimmed_listings], indent=4)}")
                            orders_request = self.create_order_request(trimmed_listings, max_loan_count)
                            self.logger.info(f"Submitting order request: {orders_request}")
                            response = self.prosper_rest_service.submit_order(orders_request)
                            self.logger.info(f"Order submitted: {response.order_id}")
                            self.notification_service.send_order_notification(account, trimmed_listings, response)

                        elif trimmed_listings and len(trimmed_listings) > 0 and self.prosper_config.run_mode == "test":
                            self.logger.info("Test mode, not submitting order. Trimmed listings:")
                            self.logger.debug(f"Trimmed listings: {json.dumps([asdict(listing) for listing in trimmed_listings], indent=4)}")
                            self.notification_service.send_order_notification(account, trimmed_listings, None)

                        else:
                            self.logger.info("No listings available after trimming, skipping buy_notes.")
                    else:
                        self.logger.info("No listings matched the filter criteria.")
                        return
                else:
                    self.logger.info("No listings available to process.")
                    return
            else:
                self.logger.info("Insufficient cash available to invest, skipping buy_notes.")
                return

        except Exception as e:
            self.logger.error(f"Error retrieving listings: {e}")
            # self.notification_service.send_error_notification(traceback.format_exc())
            raise e
        return

    def account_summary(self):
        account = self.prosper_rest_service.get_account()
        self.notification_service.send_account_summary_notification(account)
