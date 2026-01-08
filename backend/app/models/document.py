from sqlalchemy import Column, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    template_id = Column(String(100), nullable=False)
    name = Column(String(500), nullable=False)
    data = Column(JSON, nullable=False)  # Form data used to generate document
    pdf_url = Column(String(1000), nullable=True)
    paid = Column(Boolean, default=False)
    payment_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="documents")


class DocumentTemplate(Base):
    """
    Store document templates metadata.
    Templates are primarily defined in code, but this can store custom templates.
    """
    __tablename__ = "document_templates"
    
    id = Column(String(100), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    category = Column(String(50), nullable=False)
    price = Column(String(50), nullable=False)  # "free", "included", or numeric value
    icon = Column(String(50), nullable=True)
    fields = Column(JSON, nullable=False)  # Field definitions
    template_content = Column(String, nullable=True)  # Jinja2 template
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

