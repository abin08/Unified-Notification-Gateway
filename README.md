# Unified-Notification-Gateway


### Run Celery workers
```bash
celery -A app.core.celery_app worker -l info

In Mac OS Dev Environment
celery -A app.core.celery_app worker -l info --pool=solo
```

### Run FastAPI (Dev)
```bash
uvicorn app.main:app --reload
```