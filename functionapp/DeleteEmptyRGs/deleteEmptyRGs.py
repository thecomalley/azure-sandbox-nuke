import datetime
import logging
import os

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient


def delete_rgs():
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    credentials = DefaultAzureCredential()
    client = ResourceManagementClient(credentials, subscription_id)

    for rg in client.resource_groups.list():
        resoruces = client.resources.list_by_resource_group(rg.name)
        if any(resoruces) == False:
            logging.info(f"deleting empty rg: {rg.name}")
            client.resource_groups.begin_delete(rg.name)