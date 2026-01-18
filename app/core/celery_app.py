from celery import Celery

from app.core.config import settings


celery_worker = Celery(
    "ung_celery_app",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['app.workers.tasks'],
)

# Ensure tasks are not lost if the worker crashes mid-execution
celery_worker.conf.task_acks_late = True
