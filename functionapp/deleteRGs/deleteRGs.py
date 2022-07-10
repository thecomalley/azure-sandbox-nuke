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
    un_deleted_rgs = []
    deleted_rgs = []

    for rg in client.resource_groups.list():
        if "oma" not in rg.name:
            transient_rgs.append(rg.name)
            
            if os.environ.get("MODE") == "desctructive":
                try:
                    logging.info(f"Deleting rg: {rg.name}")
                    client.resource_groups.begin_delete(rg.name)

                except Exception as e:
                    logging.exception(e)
                    un_deleted_rgs.append(rg.name)
                
                else:
                    deleted_rgs.append(rg.name)

    return deleted_rgs, un_deleted_rgs