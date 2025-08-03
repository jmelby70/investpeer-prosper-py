import base64
import binascii
import logging
import os
import traceback

import yaml

import functions_framework

from config.prosper_config import ProsperConfig
from model.filterset import FilterSetProperties, FilterSet
from service.notification_service import NotificationService
from service.prosper_notes_service import ProsperNotesService


# Register a CloudEvent function with the Functions Framework
@functions_framework.cloud_event
def receive_message_function(cloud_event):
    logger.info(f"Cloud Event Received: {cloud_event}")
    event_type = get_and_decode_data_data(cloud_event.data)
    logger.info(f"Event Type: {event_type}")
    logger.info("Run mode: " + prosper_config.run_mode)
    try:
        if event_type == "buy_notes":
            prosper_notes_service.buy_notes()
        elif event_type == "account_summary":
            prosper_notes_service.account_summary()
        else:
            logger.error(f"Unknown event type: {event_type}")
            raise ValueError(f"Unknown event type: {event_type}")
    except Exception as e:
        logger.error(f"Error processing {event_type} event: {e}")
        notification_service.send_error_notification(traceback.format_exc())
        raise e
    return


def load_filterset_properties(yaml_path: str) -> FilterSetProperties:
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    filtersets = data.get("filter-set-list", {})
    filter_set_list = [FilterSet(**fs) for fs in filtersets]
    return FilterSetProperties(filter_set_list=filter_set_list)


def get_and_decode_data_data(message: dict):
    try:
        data_field = message["data"]
        logger.debug(f"Data field found in message: {data_field}")
        logger.debug(f"Encoded data: {data_field}")
        decoded = base64.b64decode(data_field, validate=True)
        logger.debug(f"Decoded data: {decoded}")
        return decoded.decode("utf-8")
    except (KeyError, TypeError, binascii.Error) as e:
        logger.error(f"Failed to decode data from message: {e}")
        logger.error(traceback.format_exc())
        return None


# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

if os.environ.get("K_SERVICE"):
    from google.cloud import logging as cloud_logging

    cloud_logging_client = cloud_logging.Client()
    cloud_logging_client.setup_logging()

logger = logging.getLogger(__name__)
logger.info("Logging initialized")

# Initialize Prosper configuration and service
prosper_config = ProsperConfig()
prosper_config.filter_set_properties = load_filterset_properties("config/filterset.yml")
logger.debug(f"Filter set properties loaded: {prosper_config.filter_set_properties}")
prosper_notes_service = ProsperNotesService(prosper_config)
notification_service = NotificationService(prosper_config)
