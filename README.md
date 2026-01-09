# 🏛️ LegalBot - Asistente Legal Inteligente para Perú

![LegalBot](https://img.shields.io/badge/LegalBot-v1.2.0-blue)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql)

> Democratizando el acceso a la justicia en el Perú con Inteligencia Artificial avanzada (RAG).

## 📋 Descripción

LegalBot es una plataforma de vanguardia que ofrece asesoría legal especializada en la legislación peruana. Utilizando un sistema de **Generación Aumentada por Recuperación (RAG)** y procesamiento de lenguaje natural de última generación, LegalBot ayuda a ciudadanos y profesionales a navegar el complejo sistema legal peruano de manera inteligente.

## 🌟 Funcionalidades de IA Avanzada

*   📂 **Analizador de PDFs en tiempo Real**: Sube contratos o notificaciones; la IA extrae el contexto legal usando **PyMuPDF** para darte respuestas precisas.
*   ⚖️ **Simulación de Audiencia (Modo Juez)**: Pon a prueba tus argumentos. La IA asume el rol de Juez, evalúa tu caso y cita jurisprudencia basándose en modelos de razonamiento avanzado.
*   🧠 **Razonamiento con Base Legal**: Gracias a técnicas de *Chain-of-Thought*, la IA identifica leyes y artículos específicos antes de emitir una recomendación.

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| **Frontend** | **React 18**, **Next.js 14** (App Router), TypeScript, Tailwind CSS |
| **Backend** | **FastAPI** (Python 3.11), SQLAlchemy, Pydantic, HTTPX |
| **Inteligencia Artificial** | **Groq (Llama 3)**, Gemini Pro, RAG (Retrieval-Augmented Generation) |
| **Bases de Datos** | **PostgreSQL (Supabase)**, **Pinecone** (Búsqueda Vectorial) |
| **Infraestructura** | Docker (Local), Render (Backend), Vercel (Frontend) |

## ⚙️ Características Técnicas

- 💬 **Chat Dinámico**: Mensajería en tiempo real con componentes de **framer-motion** y **shadcn/ui**.
- 📄 **Generación de Escritos**: Creación automatizada de documentos legales descargables.
- 🔒 **Seguridad**: Autenticación JWT y variables de entorno protegidas para producción.
- 🔍 **Embeddings Locales**: Uso de **FastEmbed** para procesamiento vectorial eficiente.

---

## ☁️ Despliegue

La aplicación se encuentra desplegada y operativa:
- **Frontend:** [legal-bot.vercel.app](https://legal-bot.vercel.app)
- **Backend:** [legalbot-dpm4.onrender.com](https://legalbot-dpm4.onrender.com)

---
Desarrollado con ❤️ para transformar el acceso legal en el Perú.
