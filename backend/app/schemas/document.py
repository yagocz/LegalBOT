from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID


class DocumentField(BaseModel):
    name: str
    label: str
    type: str
    required: bool
    placeholder: Optional[str] = None
    options: Optional[List[str]] = None


class DocumentTemplateResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    price: str | int
    icon: str
    fields: List[DocumentField]


class DocumentCreate(BaseModel):
    template_id: str
    data: Dict[str, Any]


class DocumentResponse(BaseModel):
    id: UUID
    template_id: str
    name: str
    data: Dict[str, Any]
    pdf_url: Optional[str]
    paid: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class DocumentGenerateRequest(BaseModel):
    template_id: str
    data: Dict[str, str]


class DocumentGenerateResponse(BaseModel):
    id: UUID
    name: str
    pdf_url: str
    preview_content: str

