import os
import logging
import requests


PUSHOVER_API_TOKEN = os.environ.get("PUSHOVER_API_TOKEN")
PUSHOVER_USER_KEY = os.environ.get("PUSHOVER_USER_KEY")

def send_pushover_notification(message: str) -> None:
    """
    Sends a notification to a Pushover user.

    Args:
        user_key (str): The Pushover user key.
        api_token (str): The Pushover API token.
        message (str): The message to send.

    Returns:
        None
    """
    url = "https://api.pushover.net/1/messages.json"
    payload = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send notification: {e}")
        logging.info(
            f"Response: {response.status_code} - {response.text}")
    else:
        logging.info("Notification sent successfully.")
