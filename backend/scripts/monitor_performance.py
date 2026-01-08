
import asyncio
import time
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load env vars
load_dotenv()

async def test_components():
    print("="*60)
    print("DIAGNOSTICO DE VELOCIDAD (RAG)")
    print("="*60 + "\n")

    # 1. Test FastEmbed
    print("TESTING FASTEMBED (CPU Local)")
    try:
        t0 = time.time()
        print("   Loading model...", end="", flush=True)
        from fastembed import TextEmbedding
        model = TextEmbedding(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        load_time = time.time() - t0
        print(f" Done! ({load_time:.2f}s)")
        
        t1 = time.time()
        print("   Generating embedding...", end="", flush=True)
        embedding = list(model.embed(["Esto es una prueba de velocidad."]))[0].tolist()
        embed_time = time.time() - t1
        print(f" Done! ({embed_time:.2f}s)")
        
        if embed_time > 2.0:
            print("   ⚠️  WARNING: Embeddings are slow. Is your CPU busy?")
        else:
            print("   ✅ FastEmbed es rápido.")
            
    except Exception as e:
        print(f"\n   ❌ Error FastEmbed: {e}")
        return

    # 2. Test Pinecone
    print("\nTESTING PINECONE (Network)")
    try:
        t2 = time.time()
        print("   Connecting...", end="", flush=True)
        from pinecone import Pinecone
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pc.Index("legalbot-local-384")
        print(" Connected.")
        
        print("   Searching...", end="", flush=True)
        results = index.query(vector=embedding, top_k=3, include_metadata=False)
        pinecone_time = time.time() - t2
        print(f" Done! ({pinecone_time:.2f}s)")
        
        if pinecone_time > 3.0:
            print("   ⚠️  WARNING: Pinecone connection is slow.")
        else:
            print("   ✅ Pinecone responde bien.")
            
    except Exception as e:
        print(f"\n   ❌ Error Pinecone: {e}")

    # 3. Test Groq
    print("\nTESTING GROQ LLM (Network + API)")
    try:
        t3 = time.time()
        print("   Sending request...", end="", flush=True)
        from app.services.llm_providers import GroqProvider
        groq = GroqProvider()
        # Verify model
        print(f" (Model: {groq.model}) ", end="")
        
        response = await groq.chat([{"role": "user", "content": "Hola, responde con una sola palabra."}])
        groq_time = time.time() - t3
        print(f" Done! ({groq_time:.2f}s)")
        print(f"   Response: {response}")
        
        if groq_time > 5.0:
            print("    WARNING: Groq is acting slow.")
        else:
            print("   Groq responde rápido.")

    except Exception as e:
        print(f"\n   Error Groq: {e} (Check settings.GROQ_API_KEY)")

    print("\n" + "="*60)
    print("RESULTADO FINAL")
    print("="*60)
    print("Si todos los pasos anteriores fueron rápidos (<2s), el problema está en otro lado.")
    print("Si alguno falló o tardó mucho, ahí está tu cuello de botella.")

if __name__ == "__main__":
    asyncio.run(test_components())
