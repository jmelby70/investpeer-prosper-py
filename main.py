import base64
import json
import logging
import os
from dataclasses import asdict

import functions_framework

from config.prosper_config import ProsperConfig
from service.listings_rest_service import ListingsRestService
from service.prosper_rest_service import OauthTokenHolder


# Register a CloudEvent function with the Functions Framework
@functions_framework.cloud_event
def receive_message_function(cloud_event):
    # decoded_bytes = base64.b64decode(cloud_event.data)
    # message = decoded_bytes.decode("utf-8")
    logger.info(f"Message Received: {cloud_event.data}")
    prosper_config = ProsperConfig()
    oauth_token_holder = OauthTokenHolder()
    listings_rest_service = ListingsRestService(prosper_config, oauth_token_holder)
    try:
        listings = listings_rest_service.get_listings()
        logger.info("Listings retrieved successfully.")
        logger.info(f"Total listings retrieved: {len(listings.result)}")
        logger.debug(f"Listings:\n{json.dumps(asdict(listings), indent=4)}")
    except Exception as e:
        logger.error(f"Error retrieving listings: {e}")
        raise e
    return


# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

if os.environ.get("K_SERVICE"):
    from google.cloud import logging as cloud_logging
    cloud_logging_client = cloud_logging.Client()
    cloud_logging_client.setup_logging()

logger = logging.getLogger(__name__)
logger.info("Logging initialized")
