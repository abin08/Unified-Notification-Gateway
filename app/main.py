from fastapi import FastAPI

from app.api.v1.router import router
from app.core.config import settings


app = FastAPI(description=settings.PROJECT_NAME)
app.include_router(router, prefix=settings.API_V1_STR)


@app.get("/health")
def health():
    return {"status": "healthy"}
