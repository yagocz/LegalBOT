import fitz  # PyMuPDF
import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_bytes: bytes) -> Optional[str]:
    """
    Extrae el texto de un archivo PDF proporcionado en bytes.
    """
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()
        
        # Limpieza básica
        cleaned_text = " ".join(full_text.split())
        return cleaned_text if cleaned_text else None
    except Exception as e:
        logger.error(f"Error extrayendo texto del PDF del usuario: {e}")
        return None
