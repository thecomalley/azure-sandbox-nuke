import datetime
import logging

import azure.functions as func

from DeleteEmptyRGs.deleteEmptyRGs import delete_rgs


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    # Acquire the logger for a library (azure.mgmt.resource in this example)
    logger = logging.getLogger('azure.mgmt.resource')

    # Set the desired logging level
    logger.setLevel(logging.INFO)

    delete_rgs()

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
