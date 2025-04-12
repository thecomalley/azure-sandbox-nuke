import azure.functions as func
import datetime
import json
import logging

from cleaner import clean_resource_groups

app = func.FunctionApp()


@app.timer_trigger(schedule="0 0 20 * * *", arg_name="myTimer", run_on_startup=True,
                   use_monitor=False)
def clean_rgs(myTimer: func.TimerRequest) -> None:

    if myTimer.past_due:
        logging.info('The timer is past due!')
    clean_resource_groups()
    logging.info('Python timer trigger function executed.')
