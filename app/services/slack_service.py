import requests

from app.services.base import BaseNotifier
from app.schemas.notification import SlackNotification
from app.core.config import Settings


class SlackNotifier(BaseNotifier):
    """
    Concrete implementation of the BaseNotifier for sending messages to Slack.
    Uses Incoming Webhooks.
    """

    def __init__(self, config: Settings):
        self.config = config

    def send(self, notification: SlackNotification):
        """
        Sends a message to a Slack channel via Webhook.

        Args:
            notification (SlackNotification): The payload containing the
                                            webhook_url and the text message.

        Raises:
            requests.exceptions.HTTPError: If Slack returns a non-200 status.
        """
        # Pydantic HttpUrl must be converted to string for requests
        webhook_url = str(notification.recipient.webhook_url)
        payload = {"text": notification.content.text}

        # Prepare proxies dictionary only if settings are defined
        proxies = {}
        if self.config.HTTP_PROXY:
            proxies["http"] = self.config.HTTP_PROXY
        if self.config.HTTPS_PROXY:
            proxies["https"] = self.config.HTTPS_PROXY

        response = requests.request(
            "POST", webhook_url, json=payload, proxies=proxies, timeout=10
        )
        response.raise_for_status()

        if response.status_code == 200:
            return True
