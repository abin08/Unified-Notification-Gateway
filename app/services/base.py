from abc import ABC, abstractmethod
from app.schemas.notification import NotificationRequest


class BaseNotifier(ABC):

    @abstractmethod
    def send(self, notification: NotificationRequest):
        """
        Send the notification to the downstream provider.
        Must be implemented by concrete classes.
        """
        pass
