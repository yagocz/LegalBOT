from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.conversation import LegalCategory


class LegalSource(BaseModel):
    text: str
    law: str
    article: str
    category: str


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    conversation_id: Optional[UUID] = None
    user_context: Optional[str] = None  # Text extracted from user uploaded PDF
    mode: str = "advisor"  # "advisor" or "hearing"


class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    sources: Optional[List[LegalSource]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: UUID
    title: Optional[str]
    category: LegalCategory
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    
    class Config:
        from_attributes = True


class ConversationDetailResponse(ConversationResponse):
    messages: List[MessageResponse] = []


class ChatResponse(BaseModel):
    message: MessageResponse
    conversation: ConversationResponse
    needs_lawyer: bool = False
    confidence: float = 0.0


class FeedbackRequest(BaseModel):
    message_id: UUID
    feedback: str = Field(..., pattern="^(positive|negative)$")

