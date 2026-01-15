from typing import Type

from app.core.config import settings
from app.services.base import BaseNotifier
from app.services.email_service import EmailNotifier
from app.services.slack_service import SlackNotifier


class NotifierFactory:
    """
    Factory class to instantiate the correct notification service
    based on the requested channel.
    """

    # Registry of supported channels mapping to their concrete classes
    _NOTIFIER_CLASSES: dict[str, Type[BaseNotifier]] = {
        "email": EmailNotifier,
        "slack": SlackNotifier,
    }

    @staticmethod
    def get_notifier(channel: str) -> BaseNotifier:
        """
        Returns an instance of the requested notifier initialized with global
        settings.

        Args:
            channel (str): The channel identifier (e.g., 'email', 'slack').

        Returns:
            BaseNotifier: An instance of a concrete notifier class.

        Raises:
            ValueError: If the channel is not supported.
        """
        notifier_class = NotifierFactory._NOTIFIER_CLASSES.get(channel)

        if not notifier_class:
            raise ValueError(f"Unsupported notification channel: {channel}")

        # Instantiate the class with the global application settings
        return notifier_class(config=settings)
