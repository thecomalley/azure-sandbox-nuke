import logging
import os

from azure.mgmt.resource import ResourceManagementClient
from azure.identity import DefaultAzureCredential

from pushover import send_pushover_notification

# Suppress Azure SDK logging to avoid clutter
az_log = logging.getLogger('azure')
az_log.setLevel(logging.WARNING)

# Set up this scripts logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load Environment Variables (these should be set in the Azure Function App settings)
TAG_KEY = os.environ.get("TAG_KEY")
SUBSCRIPTION_IDS_TO_CLEAN = os.environ.get("SUBSCRIPTION_IDS_TO_CLEAN")

def clean_sub_rgs(subscription_id: str) -> tuple:
    """
    Cleans up all resource groups in the given subscription, that are missing a specific tag key.
    Args:
        subscription_id (str): The Azure subscription ID to clean up.
    Returns:
        tuple: A tuple containing two lists:
            - deleted_resource_groups: List of resource groups that were deleted.
            - errored_resource_groups: List of resource groups that could not be deleted due to errors.
    """
    credentials = DefaultAzureCredential()
    azurerm = ResourceManagementClient(credentials, subscription_id)

    # list all resource groups
    resource_groups = azurerm.resource_groups.list()

    deleted_resource_groups = []
    errored_resource_groups = []

    for resource_group in resource_groups:
        # Check if the resource group has any tags
        if resource_group.tags is None:
            logger.info(
                f"Resource group {resource_group.name} has no tags.")
            resource_group.tags = {}

        # Check if the resource group has the tag key
        if TAG_KEY not in resource_group.tags:
            try:
                azurerm.resource_groups.begin_delete(resource_group.name)
            except Exception as e:
                errored_resource_groups.append(resource_group.name)
                logger.error(
                    f"Failed to delete resource group {resource_group.name}: {e}")
                continue
            else:
                deleted_resource_groups.append(resource_group.name)
                logger.info(
                    f"deleted resource group: {resource_group.name}")

    return (deleted_resource_groups, errored_resource_groups)


def clean_resource_groups() -> None:
    """
    Cleans up all resource groups in all subscriptions.
    """
    # Ensure TAG_KEY is set
    if TAG_KEY is None:
        logger.error("TAG_KEY environment variable is not set.")
        raise ValueError("TAG_KEY environment variable is not set.")
        
    subscription_ids = SUBSCRIPTION_IDS_TO_CLEAN.split(",")
    logger.info(subscription_ids)
    deleted_resource_groups = []
    errored_resource_groups = []

    for subscription_id in subscription_ids:
        logger.info(
            f"Cleaning resource groups in subscription: {subscription_id}")
        deleted_rgs, errored_rgs = clean_sub_rgs(subscription_id)
        deleted_resource_groups.extend(deleted_rgs)
        errored_resource_groups.extend(errored_rgs)

    # Send notification
    message = f"Deleted resource groups: {deleted_resource_groups}"
    if errored_resource_groups:
        message += f"\nErrored resource groups: {errored_resource_groups}"
    send_pushover_notification(message)
    logger.info("Resource group cleanup completed.")


if __name__ == "__main__":
    # Run the function locally for testing
    # Note: This is just for local testing and should not be used in production.
    # In production, this function would be triggered by an Azure Function Timer Trigger.
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting resource group cleanup...")
    clean_resource_groups()
