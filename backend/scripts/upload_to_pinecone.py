"""
Script para subir los datos legales a Pinecone
Ejecutar: python -m scripts.upload_to_pinecone

Requisitos:
- pip install openai pinecone-client
- Tener OPENAI_API_KEY y PINECONE_API_KEY configurados
"""

import json
import os
import time
import unicodedata
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Verificar dependencias
try:
    from openai import OpenAI
    from pinecone import Pinecone, ServerlessSpec
except ImportError:
    print("❌ Instala las dependencias:")
    print("   pip install openai pinecone-client")
    print("   pip install pinecone-client")
    exit(1)

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN - Cambia estas variables con tus API keys
# ═══════════════════════════════════════════════════════════════
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "") # Ya no se usa para embeddings
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
INDEX_NAME = "legalbot-local-384" # Nuevo indice para dimensiones locales
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  # Modelo local gratuito
EMBEDDING_DIMENSION = 384 # Dimensión del modelo local

# ═══════════════════════════════════════════════════════════════


def check_api_keys():
    """Verificar que las API keys estén configuradas"""
    # Solo necesitamos Pinecone ahora
    if "TU_PINECONE" in PINECONE_API_KEY or not PINECONE_API_KEY:
        print("❌ Error: Configura tu PINECONE_API_KEY")
        print("   Opción 1: export PINECONE_API_KEY='...'")
        print("   Opción 2: Edita el archivo .env")
        return False
    return True


def create_index_if_not_exists(pc: Pinecone) -> any:
    """Crear índice en Pinecone si no existe"""
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    
    if INDEX_NAME not in existing_indexes:
        print(f"📦 Creando índice '{INDEX_NAME}' (Dim: {EMBEDDING_DIMENSION})...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        # Esperar a que el índice esté listo
        print("   Esperando a que el índice esté listo...")
        while not pc.describe_index(INDEX_NAME).status['ready']:
            time.sleep(1)
        print("   ✅ Índice creado y listo")
    else:
        print(f"✅ Índice '{INDEX_NAME}' ya existe")
    
    return pc.Index(INDEX_NAME)


def generate_embedding(model, text: str) -> List[float]:
    """Generar embedding con FastEmbed"""
    # FastEmbed retorna un generador, obtenemos el primer elemento
    embeddings = list(model.embed([text]))
    return embeddings[0].tolist()


def prepare_text_for_embedding(article: dict) -> str:
    """Preparar texto del artículo para generar embedding"""
    return f"""
Ley: {article.get('ley', '')}
Número: {article.get('numero_ley', '')}
Artículo: {article.get('articulo', '')}
Título: {article.get('titulo', '')}
Contenido: {article.get('texto', '')}
Categoría: {article.get('categoria', '')}
Libro: {article.get('libro', 'N/A')}
""".strip()


def sanitize_id(text: str) -> str:
    """Convertir ID a ASCII para Pinecone"""
    # Normalizar (eliminar tildes y caracteres especiales)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    # Asegurar que sea seguro
    return text.strip()


def upload_legal_data():
    """Función principal para subir datos a Pinecone"""
    print("\n" + "="*60)
    print("🚀 SUBIR DATOS LEGALES A PINECONE (LOCAL EMBEDDINGS)")
    print("="*60 + "\n")
    
    # Verificar API keys
    if not check_api_keys():
        return
    
    # Inicializar clientes
    print("🔌 Conectando a Pinecone y cargando modelo local (FastEmbed)...")
    
    try:
        from fastembed import TextEmbedding
        # Cargar modelo local
        print(f"   Cargando modelo {EMBEDDING_MODEL}...")
        # FastEmbed descarga automáticamente el modelo optimizado
        embedding_model = TextEmbedding(model_name=EMBEDDING_MODEL)
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("   pip install fastembed")
        return

    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Cargar datos legales
    data_file = Path(__file__).parent.parent / "data" / "legal_knowledge.json"
    
    if not data_file.exists():
        print(f"❌ No se encontró el archivo de datos: {data_file}")
        print("   Ejecuta primero: python -m scripts.prepare_legal_data")
        return
    
    with open(data_file, "r", encoding="utf-8") as f:
        legal_data = json.load(f)
    
    print(f"📚 Cargados {len(legal_data)} fragmentos de texto")
    
    # Crear índice
    index = create_index_if_not_exists(pc)
    
    # Procesar y subir en lotes
    batch_size = 20
    vectors_to_upsert = []
    total_processed = 0
    
    print(f"\n📤 Subiendo vectores (lotes de {batch_size})...\n")
    
    for i, article in enumerate(legal_data):
        # Mostrar progreso
        print(f"   [{i+1}/{len(legal_data)}] Procesando: {article['ley']} - {article['articulo']}")
        print(f"   [{i+1}/{len(legal_data)}] Procesando: {article.get('ley', 'N/A')} - {article.get('articulo', 'N/A')}")
        
        try:
            # Generar texto y embedding
            text = prepare_text_for_embedding(article)
            embedding = generate_embedding(embedding_model, text)
            
            # Preparar vector
            vector = {
                "id": sanitize_id(article["id"]),
                "values": embedding,
                "metadata": {
                    "ley": article.get("ley", "Desconocido"),
                    "numero_ley": article.get("numero_ley", ""),
                    "articulo": article.get("articulo", ""),
                    "titulo": article.get("titulo", ""),
                    "texto": article.get("texto", "")[:30000], # Pinecone limit is 40KB (bytes), so 30k chars is safe buffer
                    "categoria": article.get("categoria", "general"),
                    "libro": article.get("libro", ""),
                    "jurisdiction": article.get("jurisdiction", "Peru")
                }
            }
            vectors_to_upsert.append(vector)
            
            # Subir en lotes
            if len(vectors_to_upsert) >= batch_size:
                try:
                    index.upsert(vectors=vectors_to_upsert)
                    total_processed += len(vectors_to_upsert)
                    print(f"   ⬆️  Subidos {total_processed} vectores...")
                except Exception as e:
                    print(f"   ❌ Error subiendo lote: {e}")
                vectors_to_upsert = []
                time.sleep(0.5)  # Rate limiting
                
        except Exception as e:
            print(f"   ⚠️  Error en {article.get('id', 'N/A')}: {e}")
            continue
    
    # Subir vectores restantes
    if vectors_to_upsert:
        index.upsert(vectors=vectors_to_upsert)
        total_processed += len(vectors_to_upsert)
        print(f"   ⬆️  Subidos {total_processed} vectores (final)")
    
    # Verificar resultado
    time.sleep(2)  # Esperar a que se indexen
    stats = index.describe_index_stats()
    
    print("\n" + "="*60)
    print("✅ PROCESO COMPLETADO")
    print("="*60)
    print(f"   📊 Total vectores en Pinecone: {stats.total_vector_count}")
    print(f"   🗂️  Índice: {INDEX_NAME}")
    print("="*60 + "\n")


def test_search():
    """Probar búsqueda en Pinecone"""
    print("\n🔍 Probando búsqueda...\n")
    
    if not check_api_keys():
        return
    
    print("🔌 Cargando modelo local...")
    from fastembed import TextEmbedding
    embedding_model = TextEmbedding(model_name=EMBEDDING_MODEL)

    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(INDEX_NAME)
    
    # Query de prueba
    test_query = "¿Cuánto me corresponde si me despiden?"
    print(f"📝 Query: '{test_query}'")
    
    # Generar embedding de la query
    query_embedding = generate_embedding(embedding_model, test_query)
    
    # Buscar en Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=3,
        include_metadata=True
    )
    
    print(f"\n📋 Resultados encontrados: {len(results.matches)}\n")
    
    for i, match in enumerate(results.matches, 1):
        print(f"   {i}. Score: {match.score:.4f}")
        print(f"      Ley: {match.metadata.get('ley', 'N/A')}")
        print(f"      Artículo: {match.metadata.get('articulo', 'N/A')}")
        print(f"      Título: {match.metadata.get('titulo', 'N/A')}")
        print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_search()
    else:
        upload_legal_data()
        print("\n💡 Para probar la búsqueda, ejecuta:")
        print("   python -m scripts.upload_to_pinecone test\n")

