"""
Proveedores de LLM - Alternativas a OpenAI
Soporta: Groq (gratis), Google Gemini (gratis), Ollama (local), OpenAI
"""

import os
import httpx
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from app.core.config import settings


class LLMProvider(ABC):
    """Clase base para proveedores de LLM"""
    
    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.4,
        max_tokens: int = 1500
    ) -> str:
        """Enviar mensaje y obtener respuesta"""
        pass
    
    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """Generar embedding de texto"""
        pass




class GroqProvider(LLMProvider):
    """
    Groq - LLaMA 3 70B GRATIS y muy rápido
    
    Crear cuenta: https://console.groq.com
    Límites gratis: 30 requests/min, 14,400/día
    """
    
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY or ""
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "llama-3.3-70b-versatile"  
        
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.4,
        max_tokens: int = 1500
    ) -> str:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                print(f"❌ Groq API Error: {e.response.text}")
                raise e
    
    async def embed(self, text: str) -> List[float]:
        # Groq no tiene embeddings, usar alternativa local
        return await get_local_embeddings(text)




class GeminiProvider(LLMProvider):
    """
    Google Gemini - GRATIS con límites generosos
    
    Crear API Key: https://aistudio.google.com/app/apikey
    Límites gratis: 15 requests/min, 1,500/día, 1M tokens/día
    """
    
    def __init__(self):
        self.api_key = settings.GOOGLE_API_KEY or ""
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "gemini-1.5-flash"  # Gratis y rápido
        
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.4,
        max_tokens: int = 1500
    ) -> str:
        # Convertir formato OpenAI a Gemini
        gemini_messages = []
        system_instruction = None
        
        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            else:
                role = "user" if msg["role"] == "user" else "model"
                gemini_messages.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/models/{self.model}:generateContent",
                params={"key": self.api_key},
                headers={"Content-Type": "application/json"},
                json={
                    "contents": gemini_messages,
                    "systemInstruction": {"parts": [{"text": system_instruction}]} if system_instruction else None,
                    "generationConfig": {
                        "temperature": temperature,
                        "maxOutputTokens": max_tokens
                    }
                },
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
    
    async def embed(self, text: str) -> List[float]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/models/text-embedding-004:embedContent",
                params={"key": self.api_key},
                json={
                    "model": "models/text-embedding-004",
                    "content": {"parts": [{"text": text}]}
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return data["embedding"]["values"]





class OllamaProvider(LLMProvider):
    """
    Ollama - Modelos locales, 100% gratis
    
    Instalar: https://ollama.ai
    Luego: ollama pull llama3.1
    
    Requiere: 8GB RAM mínimo, 16GB recomendado
    """
    
    def __init__(self):
        self.base_url = settings.OLLAMA_URL or "http://localhost:11434"
        self.model = settings.OLLAMA_MODEL or "llama3.1"
        self.embed_model = "nomic-embed-text"
        
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.4,
        max_tokens: int = 1500
    ) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                },
                timeout=120.0  # Modelos locales pueden ser lentos
            )
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"]
    
    async def embed(self, text: str) -> List[float]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/embeddings",
                json={
                    "model": self.embed_model,
                    "prompt": text
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return data["embedding"]


class OpenAIProvider(LLMProvider):
    """OpenAI - GPT-4o, de pago"""
    
    def __init__(self):
        from openai import AsyncOpenAI
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.4,
        max_tokens: int = 1500
    ) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    async def embed(self, text: str) -> List[float]:
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding




class TogetherProvider(LLMProvider):
    """
    Together AI - $5 gratis, muchos modelos
    
    Crear cuenta: https://www.together.ai
    Modelos: Llama, Mistral, Qwen, etc.
    """
    
    def __init__(self):
        self.api_key = settings.TOGETHER_API_KEY or ""
        self.base_url = "https://api.together.xyz/v1"
        self.model = "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"
        
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.4,
        max_tokens: int = 1500
    ) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    async def embed(self, text: str) -> List[float]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/embeddings",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "togethercomputer/m2-bert-80M-8k-retrieval",
                    "input": text
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return data["data"][0]["embedding"]




# Global cache for embedding model
_embedding_model = None

import asyncio

async def get_local_embeddings(text: str) -> List[float]:
    """
    Embeddings locales usando FastEmbed, ejecutado en ThreadPool 
    para no bloquear el Event Loop de FastAPI.
    """
    global _embedding_model
    
    # Definir la función sincrónica que hace el trabajo pesado
    def _generate_sync(text_input: str):
        global _embedding_model
        if _embedding_model is None:
            # Importación lazy y setup
            from fastembed import TextEmbedding
            _embedding_model = TextEmbedding(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
            
        return list(_embedding_model.embed([text_input]))[0].tolist()

    try:
        # Ejecutar en thread pool
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _generate_sync, text)
        
    except Exception as e:
        print(f"❌ Error en FastEmbed: {e}")
        # Fallback básico si falla el modelo
        import hashlib
        vector = []
        for i in range(384):
            hash_input = f"{text}_{i}".encode()
            hash_val = int(hashlib.md5(hash_input).hexdigest(), 16)
            vector.append((hash_val % 1000) / 1000 - 0.5)
        return vector




def get_llm_provider(provider_name: Optional[str] = None) -> LLMProvider:
    """
    Obtener el proveedor de LLM configurado
    
    Prioridad:
    1. Variable de entorno LLM_PROVIDER
    2. Parámetro provider_name
    3. Detectar automáticamente según API keys disponibles
    """
    # Usar settings en lugar de os.getenv para leer del .env correctamente
    provider = provider_name or settings.LLM_PROVIDER or "auto"
    
    if provider == "auto":
        # Detectar según API keys disponibles
        if settings.GROQ_API_KEY:
            provider = "groq"
        elif settings.GOOGLE_API_KEY:
            provider = "gemini"
        elif settings.TOGETHER_API_KEY:
            provider = "together"
        elif settings.OPENAI_API_KEY:
            provider = "openai"
        else:
            provider = "ollama"  # Fallback a local
    
    providers = {
        "groq": GroqProvider,
        "gemini": GeminiProvider,
        "ollama": OllamaProvider,
        "openai": OpenAIProvider,
        "together": TogetherProvider,
    }
    
    if provider not in providers:
        raise ValueError(f"Proveedor '{provider}' no soportado. Usa: {list(providers.keys())}")
    
    print(f"[LLM] Usando proveedor: {provider.upper()}")
    return providers[provider]()


_llm_instance = None

def get_global_llm() -> LLMProvider:
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = get_llm_provider()
    return _llm_instance