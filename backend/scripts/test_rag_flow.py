
import asyncio
import sys
import os
import time
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load env vars
load_dotenv()

async def test_full_rag():
    print("="*60)
    print("🤖 TEST DE INTEGRACIÓN RAG (Simulando Chat)")
    print("="*60 + "\n")
    
    try:
        print("1. Importando servicio RAG...", end="", flush=True)
        from app.services.rag import generate_legal_response
        print(" OK.")
        
        query = "¿Qué dice la ley sobre las rondas campesinas?"
        print(f"\n2. Ejecutando consulta: '{query}'")
        print("   (Esto usa embeddings locales + Pinecone + Groq combinados)\n")
        
        t0 = time.time()
        answer, sources, category, needs_lawyer, confidence = await generate_legal_response(query)
        duration = time.time() - t0
        
        print("\n" + "="*60)
        print(f"✅ RESPUESTA GENERADA EN {duration:.2f} SEGUNDOS")
        print("="*60)
        print(f"📄 Fuentes encontradas: {len(sources)}")
        for s in sources:
            print(f"   - {s.law} ({s.article})")
            
        print("\n🤖 Respuesta del Bot:")
        print("-" * 20)
        print(answer)
        print("-" * 20)
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO EN RAG: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_full_rag())
