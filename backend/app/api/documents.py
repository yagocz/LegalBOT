"""
Documents API endpoints for LegalBot
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.document import (
    DocumentTemplateResponse,
    DocumentResponse,
    DocumentGenerateRequest,
    DocumentGenerateResponse,
    DocumentField,
)
from app.models.document import Document
from app.services.document_generator import generate_legal_document, DOCUMENT_TEMPLATES

router = APIRouter(prefix="/documents", tags=["Documents"])

# Document templates configuration
TEMPLATES_CONFIG = [
    {
        "id": "carta-reclamo",
        "name": "Carta de Reclamo Simple",
        "description": "Documento formal para presentar un reclamo a una empresa o institución",
        "category": "consumidor",
        "price": "free",
        "icon": "FileText",
        "fields": [
            {"name": "nombreCompleto", "label": "Tu nombre completo", "type": "text", "required": True},
            {"name": "dni", "label": "DNI", "type": "text", "required": True},
            {"name": "direccion", "label": "Tu dirección", "type": "text", "required": True},
            {"name": "empresa", "label": "Empresa a reclamar", "type": "text", "required": True},
            {"name": "motivo", "label": "Motivo del reclamo", "type": "textarea", "required": True},
            {"name": "hechos", "label": "Descripción de los hechos", "type": "textarea", "required": True},
            {"name": "peticion", "label": "¿Qué solicitas?", "type": "textarea", "required": True},
        ],
    },
    {
        "id": "carta-notarial",
        "name": "Carta Notarial de Intimación",
        "description": "Carta formal para exigir el cumplimiento de una obligación",
        "category": "civil",
        "price": 49,
        "icon": "ScrollText",
        "fields": [
            {"name": "nombreCompleto", "label": "Tu nombre completo", "type": "text", "required": True},
            {"name": "dni", "label": "DNI", "type": "text", "required": True},
            {"name": "direccion", "label": "Tu dirección", "type": "text", "required": True},
            {"name": "destinatario", "label": "Nombre del destinatario", "type": "text", "required": True},
            {"name": "direccionDestinatario", "label": "Dirección del destinatario", "type": "text", "required": True},
            {"name": "hechos", "label": "Descripción de los hechos", "type": "textarea", "required": True},
            {"name": "monto", "label": "Monto adeudado (si aplica)", "type": "number", "required": False},
            {"name": "plazo", "label": "Plazo para cumplir (días)", "type": "number", "required": True},
        ],
    },
    {
        "id": "contrato-alquiler",
        "name": "Contrato de Alquiler de Vivienda",
        "description": "Contrato completo para arrendamiento de inmueble",
        "category": "civil",
        "price": 79,
        "icon": "Home",
        "fields": [
            {"name": "arrendador", "label": "Nombre del arrendador (dueño)", "type": "text", "required": True},
            {"name": "dniArrendador", "label": "DNI del arrendador", "type": "text", "required": True},
            {"name": "arrendatario", "label": "Nombre del arrendatario (inquilino)", "type": "text", "required": True},
            {"name": "dniArrendatario", "label": "DNI del arrendatario", "type": "text", "required": True},
            {"name": "direccionInmueble", "label": "Dirección del inmueble", "type": "text", "required": True},
            {"name": "montoRenta", "label": "Monto de renta mensual (S/.)", "type": "number", "required": True},
            {"name": "duracion", "label": "Duración del contrato (meses)", "type": "number", "required": True},
            {"name": "garantia", "label": "Meses de garantía", "type": "number", "required": True},
            {"name": "fechaInicio", "label": "Fecha de inicio", "type": "date", "required": True},
        ],
    },
]


@router.get("/templates", response_model=List[DocumentTemplateResponse])
async def list_templates():
    """List all available document templates"""
    return [
        DocumentTemplateResponse(
            id=t["id"],
            name=t["name"],
            description=t["description"],
            category=t["category"],
            price=t["price"],
            icon=t["icon"],
            fields=[DocumentField(**f) for f in t["fields"]],
        )
        for t in TEMPLATES_CONFIG
    ]


@router.get("/templates/{template_id}", response_model=DocumentTemplateResponse)
async def get_template(template_id: str):
    """Get a specific document template"""
    template = next((t for t in TEMPLATES_CONFIG if t["id"] == template_id), None)
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template no encontrado"
        )
    
    return DocumentTemplateResponse(
        id=template["id"],
        name=template["name"],
        description=template["description"],
        category=template["category"],
        price=template["price"],
        icon=template["icon"],
        fields=[DocumentField(**f) for f in template["fields"]],
    )


@router.post("/generate", response_model=DocumentGenerateResponse)
async def generate_document(
    request: DocumentGenerateRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate a legal document"""
    user_id = UUID(current_user["user_id"])
    
    # Validate template exists
    template = next((t for t in TEMPLATES_CONFIG if t["id"] == request.template_id), None)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template no encontrado"
        )
    
    # Check if paid template and user hasn't paid
    # In production, this would check user's subscription and payment status
    is_paid = template["price"] not in ["free", "included"]
    
    try:
        # Generate document
        pdf_buffer, preview_content = await generate_legal_document(
            request.template_id,
            request.data,
            add_watermark=is_paid,  # Add watermark if not paid
        )
        
        # Save document record
        document = Document(
            user_id=user_id,
            template_id=request.template_id,
            name=f"{template['name']} - {request.data.get('nombreCompleto', request.data.get('arrendador', 'Usuario'))}",
            data=request.data,
            paid=not is_paid,
        )
        db.add(document)
        await db.commit()
        await db.refresh(document)
        
        return DocumentGenerateResponse(
            id=document.id,
            name=document.name,
            pdf_url=f"/api/documents/{document.id}/download",
            preview_content=preview_content,
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar documento: {str(e)}"
        )


@router.get("/{document_id}/download")
async def download_document(
    document_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Download a generated document"""
    user_id = UUID(current_user["user_id"])
    
    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.user_id == user_id
        )
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )
    
    # Regenerate PDF for download
    try:
        pdf_buffer, _ = await generate_legal_document(
            document.template_id,
            document.data,
            add_watermark=not document.paid,
        )
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={document.name}.pdf"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al descargar documento: {str(e)}"
        )


@router.get("/", response_model=List[DocumentResponse])
async def list_user_documents(
    skip: int = 0,
    limit: int = 20,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List user's generated documents"""
    user_id = UUID(current_user["user_id"])
    
    result = await db.execute(
        select(Document)
        .where(Document.user_id == user_id)
        .order_by(Document.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    documents = result.scalars().all()
    
    return [
        DocumentResponse(
            id=doc.id,
            template_id=doc.template_id,
            name=doc.name,
            data=doc.data,
            pdf_url=f"/api/documents/{doc.id}/download",
            paid=doc.paid,
            created_at=doc.created_at,
        )
        for doc in documents
    ]

@router.post("/extract/{template_id}")
async def extract_document_data(
    template_id: str,
    conversation_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Extract document data from chat history using AI"""
    from app.models.conversation import Message
    from app.services.ai_documents import extract_fields_from_chat
    
    # 1. Get messages from conversation
    result = await db.execute(
        select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
    )
    messages = result.scalars().all()
    
    if not messages:
        return {"data": {}}
        
    chat_history = [{"role": m.role.value, "content": m.content} for m in messages]
    
    # 2. Call AI extraction
    extracted_data = await extract_fields_from_chat(template_id, chat_history)
    
    return {"data": extracted_data}
