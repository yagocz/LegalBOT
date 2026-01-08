"""
Chat API endpoints for LegalBot
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_user, get_current_user_optional
from app.schemas.chat import (
    MessageCreate,
    MessageResponse,
    ConversationResponse,
    ConversationDetailResponse,
    ChatResponse,
    FeedbackRequest,
    LegalSource,
)
from app.models.conversation import Conversation, Message, MessageRole, LegalCategory
from app.services.rag import generate_legal_response, generate_conversation_title
from app.services.user_docs import extract_text_from_pdf
from fastapi import UploadFile, File

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: MessageCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Send a message and get an AI response.
    Creates a new conversation if conversation_id is not provided.
    """
    user_id = UUID(current_user["user_id"])
    
    # Get or create conversation
    conversation = None
    if request.conversation_id:
        result = await db.execute(
            select(Conversation).where(
                Conversation.id == request.conversation_id,
                Conversation.user_id == user_id
            )
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversación no encontrada"
            )
    
    # Get conversation history if exists
    conversation_history = []
    if conversation:
        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at)
        )
        messages = result.scalars().all()
        conversation_history = [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
        ]
    
    # Generate AI response
    answer, sources, category, needs_lawyer, confidence = await generate_legal_response(
        request.content,
        conversation_history,
        user_context=request.user_context,
        mode=request.mode
    )
    
    # Create conversation if new
    if not conversation:
        title = await generate_conversation_title(request.content)
        conversation = Conversation(
            user_id=user_id,
            title=title,
            category=category,
        )
        db.add(conversation)
        await db.flush()
    
    # Save user message
    user_message = Message(
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=request.content,
    )
    db.add(user_message)
    
    # Save assistant message
    sources_dict = [source.model_dump() for source in sources] if sources else None
    assistant_message = Message(
        conversation_id=conversation.id,
        role=MessageRole.ASSISTANT,
        content=answer,
        sources=sources_dict,
    )
    db.add(assistant_message)
    
    await db.commit()
    await db.refresh(conversation)
    await db.refresh(assistant_message)
    
    # Get message count
    count_result = await db.execute(
        select(func.count(Message.id)).where(Message.conversation_id == conversation.id)
    )
    message_count = count_result.scalar() or 0
    
    return ChatResponse(
        message=MessageResponse(
            id=assistant_message.id,
            conversation_id=conversation.id,
            role=assistant_message.role.value,
            content=assistant_message.content,
            sources=[LegalSource(**s) for s in sources_dict] if sources_dict else None,
            created_at=assistant_message.created_at,
        ),
        conversation=ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            category=conversation.category,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            message_count=message_count,
        ),
        needs_lawyer=needs_lawyer,
        confidence=confidence,
    )


# ═══════════════════════════════════════════════════════════════
# PUBLIC DEMO ENDPOINT (No authentication required)
# ═══════════════════════════════════════════════════════════════

from pydantic import BaseModel

class DemoMessageRequest(BaseModel):
    content: str
    user_context: Optional[str] = None
    mode: str = "advisor"

class DemoMessageResponse(BaseModel):
    content: str
    sources: Optional[List[LegalSource]] = None
    category: str
    needs_lawyer: bool = False
    confidence: float = 0.0

@router.post("/demo", response_model=DemoMessageResponse)
async def demo_chat(request: DemoMessageRequest):
    """
    Public demo endpoint - no authentication required.
    For testing the AI without logging in.
    """
    # Generate AI response without saving to database
    answer, sources, category, needs_lawyer, confidence = await generate_legal_response(
        request.content,
        conversation_history=None,
        user_context=request.user_context,
        mode=request.mode
    )
    
    return DemoMessageResponse(
        content=answer,
        sources=sources,
        category=category.value,
        needs_lawyer=needs_lawyer,
        confidence=confidence,
    )


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    skip: int = 0,
    limit: int = 20,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List user's conversations"""
    user_id = UUID(current_user["user_id"])
    
    result = await db.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .offset(skip)
        .limit(limit)
    )
    conversations = result.scalars().all()
    
    # Get message counts
    response = []
    for conv in conversations:
        count_result = await db.execute(
            select(func.count(Message.id)).where(Message.conversation_id == conv.id)
        )
        message_count = count_result.scalar() or 0
        
        response.append(ConversationResponse(
            id=conv.id,
            title=conv.title,
            category=conv.category,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=message_count,
        ))
    
    return response


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a conversation with all messages"""
    user_id = UUID(current_user["user_id"])
    
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversación no encontrada"
        )
    
    # Get messages
    messages_result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    messages = messages_result.scalars().all()
    
    return ConversationDetailResponse(
        id=conversation.id,
        title=conversation.title,
        category=conversation.category,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
        message_count=len(messages),
        messages=[
            MessageResponse(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role.value,
                content=msg.content,
                sources=[LegalSource(**s) for s in msg.sources] if msg.sources else None,
                created_at=msg.created_at,
            )
            for msg in messages
        ],
    )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a conversation"""
    user_id = UUID(current_user["user_id"])
    
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversación no encontrada"
        )
    
    await db.delete(conversation)
    await db.commit()
    
    return {"message": "Conversación eliminada"}


@router.post("/feedback")
async def submit_feedback(
    request: FeedbackRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit feedback for a message"""
    result = await db.execute(
        select(Message).where(Message.id == request.message_id)
    )
    message = result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mensaje no encontrado"
        )
    
    message.feedback = request.feedback
    await db.commit()
    
    return {"message": "Feedback registrado"}


@router.post("/upload-doc")
async def upload_document(
    file: UploadFile = File(...),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Upload a PDF document and extract its text for chat context.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se admiten archivos PDF"
        )
    
    content = await file.read()
    text = extract_text_from_pdf(content)
    
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo extraer texto del PDF"
        )
    
    return {
        "filename": file.filename,
        "extracted_text": text[:10000], # Limit context to avoid token overflow
        "message": "Documento procesado correctamente"
    }

