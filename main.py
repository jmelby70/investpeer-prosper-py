import logging
import os
import yaml

import functions_framework

from config.prosper_config import ProsperConfig
from model.filterset import FilterSetProperties, FilterSet
from service.prosper_notes_service import ProsperNotesService


# Register a CloudEvent function with the Functions Framework
@functions_framework.cloud_event
def receive_message_function(cloud_event):
    logger.info(f"Message Received: {cloud_event.data}")
    logger.info("Run mode: " + os.environ.get("RUN_MODE", "test"))
    try:
        prosper_notes_service.buy_notes()
    except Exception as e:
        logger.error(f"Error processing notes: {e}")
        raise e
    return


def load_filterset_properties(yaml_path: str) -> FilterSetProperties:
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    filtersets = data.get("filter-set-list", {})
    filter_set_list = [FilterSet(**fs) for fs in filtersets]
    return FilterSetProperties(filter_set_list=filter_set_list)


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
