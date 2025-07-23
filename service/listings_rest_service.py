from model.listings import Listings
from service.prosper_rest_service import ProsperRestService
import logging


class ListingsRestService(ProsperRestService):
    def __init__(self, prosper_config, o_auth_token_holder):
        super().__init__(prosper_config, o_auth_token_holder)
        self.logger = logging.getLogger(__name__)

    def get_listings(self):
        url = f"{self.get_base_url()}/listingsvc/v2/listings?limit=5000&biddable=true&invested=false"
        global_filters = self.prosper_config.global_filters
        if global_filters:
            for key, value in global_filters.items():
                url += f"&{key}={value}"
        self.logger.info("Invoking Listings service with URL: %s", url)
        return self.get_entity(url, Listings)
