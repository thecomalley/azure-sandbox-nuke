from dataclasses import asdict
import datetime
import logging
import os

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient


logger = logging.getLogger('azure')
logger.setLevel(logging.WARNING)


def get_client():
    try:
        subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
        credentials = DefaultAzureCredential()
        client = ResourceManagementClient(credentials, subscription_id)

    except Exception as e:
        logging.error("Failed to load ResourceManagementClient")
        logging.exception(e)

    else: 
        return client


def delete_rgs():
    client = get_client()
    transient_rgs = []
    un_delteded_rgs = []
    delteded_rgs = []

    for rg in client.resource_groups.list():
        resoruces = client.resources.list_by_resource_group(rg.name)
        if "oma" not in rg.name:
            logging.info(f"Found rg: {rg.name}")
            transient_rgs.append(rg.name)
            
            if os.environ.get("MODE") == "desctructive":
                try:
                    logging.info(f"Deleting rg: {rg.name}")
                    delete_async_operation = client.resource_groups.begin_delete(rg)
                    delete_async_operation.wait()
                except Exception as e:
                    logging.error(f"Failed to delete rg: {rg}")
                    un_delteded_rgs.append(rg)
                    logging.error(e)
                else:
                    logging.info(f"Deleted rg: {rg}")
                    delteded_rgs.append(rg)

    logging.info(f"Deleted {len(delteded_rgs)} Resoruce Groups")
    if len(un_delteded_rgs) > 0:
        logging.info(f"Failed to delete {len(un_delteded_rgs)} Resoruce Groups")

    return delteded_rgs, un_delteded_rgs