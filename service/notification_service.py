# File: service/notification_service.py

import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from python_http_client.exceptions import HTTPError


class NotificationService:
    def __init__(self, prosper_config):
        self.prosper_config = prosper_config
        self.logger = logging.getLogger(__name__)

    def send_order_notification(self, account, listing_set, orders_response):
        api_key = self.prosper_config.sendgrid_api_key
        if api_key:
            from_email = From(self.prosper_config.email_from)
            to_email = To(self.prosper_config.email_to)
            subject = "Investpeer Prosper Py Order Submitted"
            content = Content("text/plain", self.get_email_body(account, listing_set, orders_response))
            mail = Mail(from_email, to_email, subject, content)
            try:
                sg = SendGridAPIClient(api_key)
                response = sg.send(mail)
                self.logger.info(f"Sent email to SendGrid with response status {response.status_code}")
            except HTTPError as e:
                self.logger.error(f"Error sending email: {e}")
        else:
            self.logger.info("No SendGrid API key configured, skipping email notification.")

    def get_email_body(self, account, listing_set, orders_response):
        sb = []
        if orders_response:
            sb.append(f"Order Number: {orders_response.order_id}")
            sb.append(f"Order Status: {orders_response.order_status}")
            sb.append(f"Order Date: {orders_response.order_date}")
        else:
            sb.append("Testing, no order submitted...")
        sb.append(f"Listing Count: {len(listing_set)}")
        order_amount = self.prosper_config.minimum_investment_amount * len(listing_set)
        sb.append(f"Total Amount: ${order_amount:,.2f}")
        sb.append(f"Available Cash Balance: ${(account.available_cash_balance - order_amount):,.2f}")
        sb.append("\nListings:")
        for listing in listing_set:
            sb.append(f"{listing.prosper_rating} {listing.listing_number}")
        return "\n".join(sb)

    def send_error_notification(self, error_message):
        api_key = self.prosper_config.sendgrid_api_key
        if api_key:
            from_email = From(self.prosper_config.email_from)
            to_email = To(self.prosper_config.email_to)
            subject = "Investpeer Prosper Py Error Notification"
            content = Content("text/plain", error_message)
            mail = Mail(from_email, to_email, subject, content)
            try:
                sg = SendGridAPIClient(api_key)
                response = sg.send(mail)
                self.logger.info(f"Sent error email to SendGrid with response status {response.status_code}")
            except HTTPError as e:
                self.logger.error(f"Error sending error email: {e}")
        else:
            self.logger.info("No SendGrid API key configured, skipping error notification.")

    def send_account_summary_notification(self, account):
        api_key = self.prosper_config.sendgrid_api_key
        if api_key:
            from_email = From(self.prosper_config.email_from)
            to_email = To(self.prosper_config.email_to)
            subject = "Investpeer Prosper Py Account Summary"
            content = Content("text/plain", self.get_account_summary_body(account))
            mail = Mail(from_email, to_email, subject, content)
            try:
                sg = SendGridAPIClient(api_key)
                response = sg.send(mail)
                self.logger.info(f"Sent account summary email to SendGrid with response status {response.status_code}")
            except HTTPError as e:
                self.logger.error(f"Error sending account summary email: {e}")
        else:
            self.logger.info("No SendGrid API key configured, skipping account summary notification.")

    def get_account_summary_body(self, account):
        sb = []
        sb.append("Account Summary")
        sb.append("=" * 40)
        sb.append(f"{'Available Cash Balance:':30} ${account.available_cash_balance:>12,.2f}")
        sb.append(f"{'Pending Investments:':30} ${account.pending_investments_primary_market:>12,.2f}")
        sb.append(f"{'Total Principal Received:':30} ${account.total_principal_received_on_active_notes:>12,.2f}")
        sb.append(f"{'Total Amount Invested:':30} ${account.total_amount_invested_on_active_notes:>12,.2f}")
        sb.append(f"{'Outstanding Principal:':30} ${account.outstanding_principal_on_active_notes:>12,.2f}")
        sb.append(f"{'Total Account Value:':30} ${account.total_account_value:>12,.2f}")
        sb.append("\nInvested Note Grades:")
        sb.append("-" * 40)
        for note_grade, amount in account.invested_notes.items():
            sb.append(f"({note_grade}):{'':12} ${amount:>12,.2f}")
        return "\n".join(sb)
