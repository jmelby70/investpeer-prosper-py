# File: service/notification_service.py

import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from python_http_client.exceptions import HTTPError


class NotificationService:
    def __init__(self, prosper_config):
        self.prosper_config = prosper_config
        self.logger = logging.getLogger(__name__)

    def send_order_notification(self, listing_set, orders_response):
        api_key = self.prosper_config.sendgrid_api_key
        if api_key:
            from_email = From(self.prosper_config.email_from)
            to_email = To(self.prosper_config.email_to)
            subject = "Investpeer Prosper Py Order Submitted"
            content = Content("text/plain", self.get_email_body(listing_set, orders_response))
            mail = Mail(from_email, to_email, subject, content)
            try:
                sg = SendGridAPIClient(api_key)
                response = sg.send(mail)
                self.logger.info(f"Sent email to SendGrid with response status {response.status_code}")
            except HTTPError as e:
                self.logger.error(f"Error sending email: {e}")
        else:
            self.logger.info("No SendGrid API key configured, skipping email notification.")

    def get_email_body(self, listing_set, orders_response):
        sb = []
        if orders_response:
            sb.append(f"Order Number: {orders_response.order_id}")
            sb.append(f"Order Status: {orders_response.order_status}")
            sb.append(f"Order Date: {orders_response.order_date}")
        else:
            sb.append("Testing, no order submitted...")
        sb.append(f"Listing Count: {len(listing_set)}")
        sb.append(f"Total Amount: ${self.prosper_config.minimum_investment_amount * len(listing_set)}")
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
