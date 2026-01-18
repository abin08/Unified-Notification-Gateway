import logging

from fastapi import APIRouter, HTTPException, status
from celery.exceptions import OperationalError

from app.schemas.notification import NotificationRequest, NotifyResponse
from app.workers.tasks import send_notification_task


router = APIRouter()
logger = logging.getLogger(__name__)

