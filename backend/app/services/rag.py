"""
RAG (Retrieval Augmented Generation) Service for Legal Queries
Sistema de IA Real para consultas legales peruanas

Soporta múltiples proveedores:
- Groq (GRATIS)
- Google Gemini (GRATIS)
- Ollama (LOCAL, GRATIS)
- OpenAI (de pago)
- Together AI ($5 gratis)
"""

import os
from typing import List, Optional, Tuple
from app.core.config import settings
from app.schemas.chat import LegalSource
from app.models.conversation import LegalCategory
from app.services.llm_providers import get_global_llm, get_local_embeddings
from app.services.ai_documents import suggest_document_template, extract_fields_from_chat

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════

# Proveedor de LLM (Lazy loading via get_global_llm)

# Cliente Pinecone (Lazy loading)
_pinecone_index = None

def get_pinecone_index():
    global _pinecone_index
    if _pinecone_index:
        return _pinecone_index
        
    try:
        from pinecone import Pinecone
        if settings.PINECONE_API_KEY and "TU_" not in settings.PINECONE_API_KEY:
            pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            _pinecone_index = pc.Index("legalbot-local-384")
            print("[OK] Pinecone conectado (Lazy Load)")
            return _pinecone_index
    except Exception as e:
        print(f"[WARN] Pinecone no disponible: {e}")
    
    return None

# ═══════════════════════════════════════════════════════════════
# PROMPT DEL SISTEMA
# ═══════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════
# PROMPT DEL SISTEMA
# ═══════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """Usted es un Agente de Inteligencia Artificial Legal de élite, especializado en el sistema jurídico peruano, con más de 20 años de experiencia.

## REGLA PRIMORDIAL
Todas sus respuestas DEBEN estar fundamentadas en el contexto legal proporcionado. NO invente leyes. Si la información no está en el contexto, dígalo explícitamente.

## COMPORTAMIENTO Y RAZONAMIENTO
1. **Análisis de Hechos**: Identifique los hechos clave de la consulta del usuario.
2. **Identificación de Norma**: Busque la norma exacta en el contexto (Constitución, Ley, Decreto).
3. **Subsunción**: Explique cómo la norma se aplica específicamente a los hechos del usuario.
4. **Cita Estricta**: No parafrasee artículos si puede citarlos textualmente.

## EJEMPLO DE RAZONAMIENTO ESPERADO (Few-Shot):
*Usuario*: "Mi jefe no me quiere pagar la CTS después de 3 meses."
*Análisis Interno*: El usuario tiene más de 1 mes de vínculo laboral. Según el D.S. 001-97-TR, el derecho se devenga desde el primer mes.
*Respuesta*: "📌 **Resumen Ejecutivo**: Usted tiene derecho al depósito de su CTS... 📋 **Análisis**: Al haber superado el primer mes... ⚖️ **Base Legal**: D.S. 001-97-TR, Artículo 2..."

## ESTRUCTURA DE LA RESPUESTA
📌 **Resumen Ejecutivo** (Directo y claro)
📋 **Análisis Jurídico** (Aplicación de la norma a los hechos)
⚖️ **Base Legal** (Cita exacta indicando Ley y Artículo)
✅ **Recomendaciones y Pasos a Seguir**
⚠️ **Aviso de Responsabilidad**

## CONTEXTO LEGAL DISPONIBLE:
{context}

Jurisdicción: {jurisdiction}
"""

HEARING_PROMPT = """Usted es un Juez de la República del Perú con amplia experiencia en procesos civiles, laborales y de familia.

## SU ROL
Su objetivo es actuar como la autoridad en una SIMULACIÓN DE AUDIENCIA. Debe evaluar los argumentos del usuario, hacer preguntas incisivas y señalar las debilidades legales en su postura.

## COMPORTAMIENTO
1. **Neutralidad Crítica**: No es el asesor del usuario. Es quien lo juzga.
2. **Interrogatorio**: Haga preguntas directas sobre los hechos y las pruebas que el usuario menciona.
3. **Lenguaje Judicial**: Use un tono extremadamente formal y solemne ("Dígale a este despacho...", "Precise usted...").
4. **Respeto a la Ley**: Use el contexto legal para rebatir o validar lo que el usuario dice.

## ESTRUCTURA DE LA RESPUESTA
🏛️ **Apertura de este Despacho**
(Respuesta breve al punto mencionado por el usuario desde la perspectiva de un juez)

🔍 **Interrogatorio de Ley**
(2-3 preguntas críticas que el usuario debe responder para ganar su caso)

⚖️ **Observación Preliminar sobre el Derecho**
(Análisis corto de cómo la ley se aplica en su contra o a su favor basado en el contexto)

## CONTEXTO LEGAL PARA EL CASO:
{context}

{user_context_block}
"""

# ═══════════════════════════════════════════════════════════════
# FUNCIONES AUXILIARES
# ═══════════════════════════════════════════════════════════════

def detect_language(text: str) -> str:
    """Simple language detection"""
    spanish_words = {"el", "la", "de", "que", "en", "es", "un", "por", "con", "para", "hola", "gracias"}
    english_words = {"the", "is", "of", "to", "and", "in", "for", "on", "with", "at", "hello", "thanks"}
    
    words = text.lower().replace('?', '').replace('!', '').split()
    spanish_count = sum(1 for w in words if w in spanish_words)
    english_count = sum(1 for w in words if w in english_words)
    
    return "es" if spanish_count >= english_count else "en"

async def needs_clarification(query: str, sources: List[LegalSource]) -> Optional[str]:
    """Check if query needs clarification before answering"""
    # Very short queries may need context
    words = query.split()
    if len(words) < 3 and not sources:
        lang = detect_language(query)
        if lang == "es":
            return "¿Podrías darme más detalles sobre tu situación específica para ayudarte mejor?"
        else:
            return "Could you provide more details about your specific situation so I can help you better?"
    
    return None

def is_greeting(query: str) -> bool:
    """Detectar si es un saludo"""
    greetings = [
        "hola", "buenos días", "buenas tardes", "buenas noches", 
        "hey", "hi", "buenas", "qué tal", "como estas", "cómo estás",
        "saludos", "que hay", "hello", "good morning"
    ]
    query_lower = query.lower().strip()
    query_clean = "".join(c for c in query_lower if c.isalnum() or c.isspace())
    query_words = set(query_clean.split())
    
    for greeting in greetings:
        if greeting in query_words or greeting == query_clean:
            return True
            
    return False

def is_thanks(query: str) -> bool:
    """Detectar agradecimientos"""
    thanks = ["gracias", "muchas gracias", "te agradezco", "thanks", "thank you", "genial", "perfecto", "cool"]
    query_lower = query.lower().strip()
    query_clean = "".join(c for c in query_lower if c.isalnum() or c.isspace())
    query_words = set(query_clean.split())
    
    for t in thanks:
        if t in query_words or t == query_clean:
            return True
    return False

def is_help_query(query: str) -> bool:
    """Detectar si pregunta qué puede hacer el bot"""
    help_patterns = [
        "que puedes", "qué puedes", "que haces", "qué haces",
        "ayuda", "ayúdame", "como funciona", "cómo funciona",
        "what can you", "help me", "how does it work"
    ]
    query_lower = query.lower()
    return any(p in query_lower for p in help_patterns)

async def generate_embedding(text: str) -> List[float]:
    """Generar embedding con el proveedor configurado"""
    try:
        # Usa provider local (Groq no tiene embeddings, usa fastembed)
        return await get_global_llm().embed(text)
    except Exception as e:
        print(f"Error generando embedding, usando local: {e}")
        return await get_local_embeddings(text)

# ═══════════════════════════════════════════════════════════════
# CONOCIMIENTO LOCAL (Fallback)
# ═══════════════════════════════════════════════════════════════

LOCAL_KNOWLEDGE = {
    "laboral": [
        {
            "text": "La indemnización por despido arbitrario es equivalente a una remuneración y media ordinaria mensual por cada año completo de servicios con un máximo de doce (12) remuneraciones.",
            "law": "D.S. 003-97-TR",
            "article": "Artículo 38"
        },
        {
            "text": "El trabajador tiene derecho a recibir su CTS dentro de las 48 horas de producido el cese.",
            "law": "D.S. 001-97-TR",
            "article": "Artículo 3"
        }
    ],
    "consumidor": [
        {
            "text": "El proveedor es responsable por la idoneidad y calidad de los productos y servicios que ofrece.",
            "law": "Código de Protección al Consumidor",
            "article": "Artículo 18"
        }
    ],
    "familia": [
        {
            "text": "Los alimentos comprenden lo necesario para el sustento, habitación, vestido, educación, instrucción y capacitación para el trabajo.",
            "law": "Código Civil",
            "article": "Artículo 472"
        }
    ],
    "general": [
        {
            "text": "LegalBot es un asistente de IA especializado en leyes peruanas. Mi propósito es guiarte en temas laborales, consumidor, familia, civil, tránsito y empresas.",
            "law": "Guía LegalBot",
            "article": "Introducción"
        },
        {
            "text": "Para casos complejos, siempre se recomienda la asesoría de un abogado titulado en el Perú.",
            "law": "Aviso Legal",
            "article": "General"
        }
    ]
}

# ═══════════════════════════════════════════════════════════════
# FUNCIONES PRINCIPALES
# ═══════════════════════════════════════════════════════════════

async def classify_query(query: str) -> LegalCategory:
    """Clasificar consulta usando palabras clave para mejorar precisión de búsqueda"""
    q = query.lower()
    
    if any(w in q for w in ["despido", "cts", "sueldo", "trabajo", "laboral", "sunafil", "vacaciones", "contrato de trabajo"]):
        return LegalCategory.LABORAL
    if any(w in q for w in ["hijo", "alimento", "pensión", "divorcio", "tenencia", "familia", "conyuge"]):
        return LegalCategory.FAMILIA
    if any(w in q for w in ["indecopi", "reclamo", "consumidor", "tienda", "producto", "garantía"]):
        return LegalCategory.CONSUMIDOR
    if any(w in q for w in ["papeleta", "multa", "tránsito", "sat", "brevete", "choque"]):
        return LegalCategory.TRANSITO
    if any(w in q for w in ["empresa", "sac", "eirl", "sociedad", "ruc", "constituir"]):
        return LegalCategory.EMPRESAS
    if any(w in q for w in ["contrato", "alquiler", "arrendamiento", "deuda", "civil", "propiedad"]):
        return LegalCategory.CIVIL
        
    return LegalCategory.GENERAL


async def search_pinecone(query: str, category: str, top_k: int = 3) -> List[dict]:
    """Buscar en Pinecone por similitud semántica"""
    index = get_pinecone_index()
    if not index:
        return []
    
    try:
        # Generar embedding de la query
        query_embedding = await generate_embedding(query)
        if not query_embedding:
            return []
        
        # Buscar en Pinecone (Ejecutar en thread pool para no bloquear)
        import asyncio
        loop = asyncio.get_running_loop()
        
        def _query_sync():
            return index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter={"category": category} if category != "general" else None
            )

        results = await loop.run_in_executor(None, _query_sync)
        
        return [
            {
                "text": match.metadata.get("texto", ""),
                "law": match.metadata.get("ley", "Documento"),
                "article": match.metadata.get("articulo", ""),
                "score": match.score,
                "jurisdiction": match.metadata.get("jurisdiction", "Peru")
            }
            for match in results.matches
            if match.score > 0.7  # Solo resultados relevantes
        ]
    except Exception as e:
        print(f"Error buscando en Pinecone: {e}")
        return []


async def retrieve_legal_context(
    query: str,
    category: LegalCategory,
    top_k: int = 5
) -> List[LegalSource]:
    """Obtener contexto legal relevante (Pinecone o fallback local)"""
    sources = []
    category_key = category.value if category != LegalCategory.GENERAL else "general"
    
    # 🚀 MEJORA: Expansión de Consulta (Query Expansion)
    # Convertimos la duda del usuario en una búsqueda técnica legal
    search_query = query
    try:
        expansion_prompt = f"Como experto legal, transforme esta consulta de usuario en una frase de búsqueda técnica para una base de datos de leyes peruanas. Responda solo con la frase técnica: '{query}'"
        search_query = await get_global_llm().chat(
            messages=[{"role": "user", "content": expansion_prompt}],
            temperature=0.0,
            max_tokens=60
        )
        print(f"🔍 [RAG] Query Expandida: {search_query}")
    except Exception as e:
        print(f"[WARN] Error expandiendo query: {e}")

    # Intentar primero con Pinecone
    if get_pinecone_index():
        pinecone_results = await search_pinecone(search_query, category_key, top_k)
        for doc in pinecone_results:
            sources.append(LegalSource(
                text=doc["text"],
                law=doc["law"],
                article=doc["article"],
                category=category_key,
            ))
    
    # Si no hay resultados de Pinecone, usar base local (Fallback)
    if not sources:
        local_docs = LOCAL_KNOWLEDGE.get(category_key, [])
        # Also search in 'general' or other cats if specific cat yielded nothing
        if not local_docs and category_key != "general":
             local_docs = LOCAL_KNOWLEDGE.get("general", [])
             
        for doc in local_docs[:top_k]:
            sources.append(LegalSource(
                text=doc["text"],
                law=doc["law"],
                article=doc["article"],
                category=category_key,
            ))
    
    return sources


def format_context(sources: List[LegalSource]) -> str:
    """Formatear fuentes legales para el prompt"""
    if not sources:
        return "No sufficient legal sources found."
    
    context_parts = ["### Relevant Legal Sources:\n"]
    for i, source in enumerate(sources, 1):
        # Handle missing article numbers by showing law/filename
        header = f"{source.law}"
        if source.article and "Artículo" in source.article:
             header += f" - {source.article}"
        
        context_parts.append(
            f"**{i}. {header}:**\n> \"{source.text}\"\n"
        )
    
    return "\n".join(context_parts)


async def detect_complexity(query: str) -> Tuple[bool, float]:
    """Detectar si necesita abogado humano (Simplified)"""
    # ... logic remains similar ...
    return False, 0.85


async def generate_legal_response(
    query: str,
    conversation_history: Optional[List[dict]] = None,
    user_context: Optional[str] = None,
    mode: str = "advisor"
) -> Tuple[str, List[LegalSource], LegalCategory, bool, float]:
    """
    Generar respuesta legal usando RAG
    """
    import time
    start_total = time.time()
    print(f"⏱️ [RAG] Inicio query: '{query[:50]}...'")

    lang = detect_language(query)
    
    # Quick responses for greetings
    if is_greeting(query) and not conversation_history:
        if lang == "es":
            return "¡Hola! Soy tu asistente legal con IA. ¿En qué puedo ayudarte hoy?", [], LegalCategory.GENERAL, False, 1.0
        else:
            return "Hello! I am your AI legal assistant. How can I help you today?", [], LegalCategory.GENERAL, False, 1.0
            
    if is_thanks(query):
        if lang == "es":
            return "¡De nada! Recuerda que esto no es consejo legal oficial.", [], LegalCategory.GENERAL, False, 1.0
        else:
            return "You're welcome! Remember this is not official legal advice.", [], LegalCategory.GENERAL, False, 1.0

    # Classify query
    category = await classify_query(query)
    print(f"🏷️ [RAG] Categoría detectada: {category.value}")

    # Retrieve context
    t0 = time.time()
    sources = await retrieve_legal_context(query, category)
    print(f"⏱️ [RAG] Retrieve context ({len(sources)} docs): {time.time() - t0:.2f}s")
    
    # Check for clarification
    clarification = await needs_clarification(query, sources)
    if clarification:
        return clarification, [], LegalCategory.GENERAL, False, 1.0

    # Build prompt
    context = format_context(sources)
    jurisdiction = "Peru"
    
    # 🚀 MEJORA: Selección de Prompt según Modo (Asesor vs Audiencia)
    if mode == "hearing":
        user_context_block = f"## DOCUMENTO DEL USUARIO (PRUEBA):\n{user_context}" if user_context else ""
        formatted_system_prompt = HEARING_PROMPT.format(
            context=context,
            user_context_block=user_context_block
        )
    else:
        # En modo asesor, incluimos el documento del usuario como parte del contexto para análisis
        if user_context:
            context += f"\n\n### Documento del Usuario Analizado:\n{user_context}"
            
        formatted_system_prompt = SYSTEM_PROMPT.format(
            context=context,
            jurisdiction=jurisdiction
        )

    messages = [{"role": "system", "content": formatted_system_prompt}]
    
    if conversation_history:
        for msg in conversation_history[-4:]: # Keep history shorter
            messages.append({"role": msg["role"], "content": msg["content"]})
    
    messages.append({"role": "user", "content": query})
    
    try:
        t1 = time.time()
        answer = await get_global_llm().chat(
            messages=messages,
            temperature=0.3, # Lower temp for more factual answers
            max_tokens=1500,
        )
        print(f"⏱️ [RAG] LLM generation: {time.time() - t1:.2f}s")

        # 🚀 MEJORA: Paso de Verificación (Self-Correction)
        # Verificamos si la respuesta es coherente con el contexto
        try:
            verify_prompt = f"Analice la respuesta generada y confirme si contradice los hechos del contexto legal proporcionado. Si es correcta, responda 'OK'. Si detecta una alucinación o error, corríjala brevemente.\n\nCONTEXTO:\n{context}\n\nRESPUESTA A VERIFICAR:\n{answer}"
            verification = await get_global_llm().chat(
                messages=[{"role": "user", "content": verify_prompt}],
                temperature=0.0,
                max_tokens=200
            )
            if "OK" not in verification:
                print(f"⚖️ [RAG] Autocorrección aplicada")
                answer = verification
        except:
             pass

        print(f"⏱️ [RAG] Total Time: {time.time() - start_total:.2f}s")
    except Exception as e:
        msg = "Error processing request. Please try again." if lang == "en" else "Error procesando la solicitud. Intenta de nuevo."
        return f"{msg} ({str(e)})", [], LegalCategory.GENERAL, True, 0.0

    needs_lawyer = True if not sources else False
    confidence = 0.5 if not sources else 0.9
    
    # 🚀 MEJORA: Sugerencia de Documentos con IA
    try:
        doc_id = await suggest_document_template(query, conversation_history or [])
        if doc_id:
            from app.api.documents import TEMPLATES_CONFIG
            template = next((t for t in TEMPLATES_CONFIG if t["id"] == doc_id), None)
            if template:
                suggestion_msg = f"\n\n---\n💡 **Sugerencia**: He detectado que podría necesitar una **{template['name']}**. Si desea, puedo ayudarle a redactarla ahora mismo."
                answer += suggestion_msg
    except Exception as e:
        print(f"[WARN] Error en sugerencia de doc: {e}")

    return answer, sources, LegalCategory.GENERAL, needs_lawyer, confidence


async def generate_conversation_title(first_message: str) -> str:
    # ... logic remains same ...
    return first_message[:30] + "..."


async def generate_conversation_title(first_message: str) -> str:
    """Generar título para la conversación"""
    try:
        response = await get_global_llm().chat(
            messages=[
                {
                    "role": "user",
                    "content": f"Genera un título corto (máximo 40 caracteres) en español para esta consulta legal. Solo responde con el título, sin comillas: {first_message[:150]}"
                }
            ],
            temperature=0.5,
            max_tokens=30,
        )
        
        title = response.strip().strip('"\'')
        return title[:40]
    except Exception:
        return first_message[:40] + "..." if len(first_message) > 40 else first_message
