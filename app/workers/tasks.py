from pydantic import TypeAdapter

from app.core.celery_app import celery_worker
from app.schemas.notification import NotificationRequest
from app.services.factory import NotifierFactory


@celery_worker.task
def send_notification_task(notification_data: dict):
    """
    Asynchronous task to process and send a notification.

    This task deserializes the raw dictionary payload into a Pydantic model,
    selects the appropriate notifier via the Factory and sends the message.
    It is designed to be idempotent and retried automatically by Celery on
    failure.

    Args:
        notification_data (dict): The JSON-compatible dictionary representation
                                  of the NotificationRequest.
    """
    model = TypeAdapter(NotificationRequest).validate_python(notification_data)
    notifier = NotifierFactory.get_notifier(model.channel)
    notifier.send(model)
