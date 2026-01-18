from typing import Literal, List, Optional, Union
from pydantic import BaseModel, EmailStr, HttpUrl, Field


class BaseMetadata(BaseModel):
    source_service: str = Field(
        ...,
        min_length=1,
        description="The calling service"
    )
    trace_id: Optional[str] = None


class SlackRecipient(BaseModel):
    webhook_url: HttpUrl


class SlackContent(BaseModel):
    text: str = Field(..., min_length=1)


class SlackNotification(BaseModel):
    channel: Literal['slack']
    recipient: SlackRecipient
    content: SlackContent
    metadata: BaseMetadata


class EmailRecipient(BaseModel):
    to: List[EmailStr]
    cc: Optional[List[EmailStr]] = None
    bcc: Optional[List[EmailStr]] = None


class EmailContent(BaseModel):
    subject: str = Field(..., min_length=1)
    html_body: str = Field(..., min_length=1)


class EmailNotification(BaseModel):
    channel: Literal['email']
    recipient: EmailRecipient
    content: EmailContent
    metadata: BaseMetadata


NotificationRequest = Union[SlackNotification, EmailNotification]


class NotifyResponse(BaseModel):
    status: str = "queued"
    request_id: str
    message: str
