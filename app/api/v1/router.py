import logging

from fastapi import APIRouter, HTTPException, status
from celery.exceptions import OperationalError

from app.schemas.notification import NotificationRequest, NotifyResponse
from app.workers.tasks import send_notification_task


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
        "/notify",
        response_model=NotifyResponse,
        status_code=status.HTTP_202_ACCEPTED
)
async def notify(request: NotificationRequest):
    """
    Ingests a notification request and queues it for asynchronous processing.

    Returns:
        202 Accepted: If the request is valid and queued.
        503 Service Unavailable: If the queue (Redis) is down.
    """
    # Serialize Pydantic model to JSON-compatible dict
    notification_data = request.model_dump(mode="json")

    try:
        # The .delay() call pushes the message to Redis
        task = send_notification_task.delay(notification_data)

        return NotifyResponse(
            request_id=task.id,
            message="Notification request accepted for processing.",
        )

    except OperationalError as e:
        # Catch specific Celery connection errors (like Redis down)
        logger.error(f"Failed to queue task: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Notification queue is currently unavailable."
        )
    except Exception as e:
        logger.error(f"Unexpected error in /notify: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
