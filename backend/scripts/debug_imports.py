
import sys
import os
import time

# Unbuffered output
sys.stdout.reconfigure(line_buffering=True)

print(f"PID: {os.getpid()}")
print("Start debugging imports...")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("Path added.")

print("1. Importing settings...")
from app.core.config import settings
print(f"   Settings loaded. Provider: {settings.LLM_PROVIDER}")

print("2. Importing llm_providers...")
import app.services.llm_providers
print("   llm_providers imported.")

print("3. Getting LLM provider...")
llm = app.services.llm_providers.get_llm_provider()
print(f"   LLM: {llm}")

print("4. Importing rag...")
import app.services.rag
print("   rag imported.")
