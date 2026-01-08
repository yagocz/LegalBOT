import asyncio
import os
import sys

# Add current directory to path to allow imports
sys.path.append(os.getcwd())

from app.core.config import settings
from app.services.llm_providers import GroqProvider, OpenAIProvider

async def main():
    print(f"Starting debug script...", flush=True)
    
    # Test Groq
    print(f"Testing Groq Provider with key: {settings.GROQ_API_KEY[:10]}...", flush=True)
    try:
        provider = GroqProvider()
        response = await provider.chat([{"role": "user", "content": "Hola"}])
        print("Groq Success!", flush=True)
        print(response, flush=True)
    except Exception as e:
        print("Groq FAILED!", flush=True)
        print(e, flush=True)

    print("-" * 20, flush=True)

    # Test OpenAI
    if settings.OPENAI_API_KEY:
        print(f"Testing OpenAI Provider with key: {settings.OPENAI_API_KEY[:10]}...", flush=True)
        try:
            settings.LLM_PROVIDER = "openai" # Force provider for factory if needed, but here we instantiate directly
            # provider = OpenAIProvider() # Need to be careful with imports inside the class
            # The class does: from openai import AsyncOpenAI inside __init__
            provider = OpenAIProvider()
            response = await provider.chat([{"role": "user", "content": "Hola"}])
            print("OpenAI Success!", flush=True)
            print(response, flush=True)
        except Exception as e:
            print("OpenAI FAILED!", flush=True)
            print(e, flush=True)
    else:
        print("No OpenAI key found.", flush=True)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
