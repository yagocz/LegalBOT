import json
import logging
from typing import Dict, Any, List, Optional
from app.services.llm_providers import get_global_llm
from app.api.documents import TEMPLATES_CONFIG

logger = logging.getLogger(__name__)

EXTRACTION_PROMPT = """Usted es un experto en extracción de datos legales.
Su tarea es analizar el historial de una conversación y extraer información específica para completar un documento legal: "{template_name}".

## CAMPOS REQUERIDOS:
{fields_description}

## INSTRUCCIONES:
1. Analice cuidadosamente el historial de chat proporcionado.
2. Extraiga los valores exactos para cada campo requerido.
3. Si un campo no ha sido mencionado, responda con nulo (null).
4. Devuelva los datos ESTRICTAMENTE en formato JSON.
5. NO invente datos. Si no existe, es null.
6. El formato de fecha debe ser YYYY-MM-DD si es posible.

## HISTORIAL DE CHAT:
{chat_history}

## RESPUESTA JSON REQUERIDA:
"""

async def extract_fields_from_chat(
    template_id: str,
    messages: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Usa la IA para extraer datos de un documento a partir del historial de chat.
    """
    # 1. Obtener la configuración del template
    template = next((t for t in TEMPLATES_CONFIG if t["id"] == template_id), None)
    if not template:
        logger.error(f"Template {template_id} no encontrado para extracción.")
        return {}

    # 2. Formatear la descripción de los campos
    fields_desc = ""
    for field in template["fields"]:
        required_str = "(Requerido)" if field.get("required") else "(Opcional)"
        fields_desc += f"- {field['name']}: {field['label']} {required_str}\n"

    # 3. Formatear el historial de chat
    history_text = ""
    for msg in messages:
        role = "Usuario" if msg["role"] == "user" else "Asistente"
        history_text += f"{role}: {msg['content']}\n\n"

    # 4. Preparar el prompt
    prompt = EXTRACTION_PROMPT.format(
        template_name=template["name"],
        fields_description=fields_desc,
        chat_history=history_text
    )

    try:
        # 5. Llamar al LLM
        response = await get_global_llm().chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1, # Muy baja temperatura para extracción precisa
            max_tokens=500
        )

        # 6. Limpiar y parsear JSON
        cleaned_response = response.strip()
        if "```json" in cleaned_response:
            cleaned_response = cleaned_response.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned_response:
            cleaned_response = cleaned_response.split("```")[1].strip()

        extracted_data = json.loads(cleaned_response)
        
        # Eliminar campos nulos
        return {k: v for k, v in extracted_data.items() if v is not None}

    except Exception as e:
        logger.error(f"Error en extracción de campos con IA: {e}")
        return {}

async def suggest_document_template(query: str, chat_history: List[Dict[str, str]]) -> Optional[str]:
    """
    Sujiere un template de documento basado en la consulta y el historial.
    """
    templates_str = ""
    for t in TEMPLATES_CONFIG:
        templates_str += f"- {t['id']}: {t['name']} ({t['description']})\n"

    prompt = f"""Analice la siguiente consulta legal y el historial. 
Determine si el usuario necesita generar uno de estos documentos específicos.
Si no hay un match claro, responda "none".
Si hay un match, responda SOLO con el ID del documento.

TEMPLATES:
{templates_str}

CONSULTA: {query}

HISTORIAL RECIENTE:
{chat_history[-2:] if chat_history else "Ninguno"}

RESPUESTA (ID o "none"):"""

    try:
        response = await get_global_llm().chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=10
        )
        result = response.strip().lower()
        
        # Validar que el ID existe
        if any(t["id"] == result for t in TEMPLATES_CONFIG):
            return result
        return None
    except:
        return None
