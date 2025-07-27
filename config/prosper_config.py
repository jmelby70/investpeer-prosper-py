import os


class ProsperConfig:
    def __init__(self):
        self.run_mode = os.environ.get("RUN_MODE", "test")
        self.client_id = os.environ.get("PROSPER_CLIENT_ID")
        self.client_secret = os.environ.get("PROSPER_CLIENT_SECRET")
        self.username = os.environ.get("PROSPER_USERNAME")
        self.password = os.environ.get("PROSPER_PASSWORD")
        self.base_url = os.environ.get("PROSPER_BASE_URL", "https://api.prosper.com")
        self.minimum_investment_amount = float(os.environ.get("PROSPER_MINIMUM_INVESTMENT_AMOUNT", 25.0))
        self.order_list_limit = int(os.environ.get("PROSPER_ORDER_LIST_LIMIT", 25))
        self.email_from = os.environ.get("PROSPER_EMAIL_FROM")
        self.email_to = os.environ.get("PROSPER_EMAIL_TO")
        self.sendgrid_api_key = os.environ.get("PROSPER_SENDGRID_API_KEY")
        self.global_filters = {
            "listing_category_id": os.environ.get("PROSPER_GLOBAL_FILTERS_LISTING_CATEGORY_ID", "1"),
            "has_mortgage": os.environ.get("PROSPER_GLOBAL_FILTERS_HAS_MORTGAGE", "true"),
            "income_range": os.environ.get("PROSPER_GLOBAL_FILTERS_INCOME_RANGE", "4,5,6"),
        }
