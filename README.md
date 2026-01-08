# 🏛️ LegalBot - Asistente Legal Inteligente para Perú

![LegalBot](https://img.shields.io/badge/LegalBot-v1.2.0-blue)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![IA](https://img.shields.io/badge/AI-Advanced_RAG-orange)

> Democratizando el acceso a la justicia en el Perú con Inteligencia Artificial avanzada.

## 📋 Descripción

LegalBot es una plataforma de vanguardia que ofrece asesoría legal especializada en la legislación peruana. Utilizando un sistema de **Generación Aumentada por Recuperación (RAG)** y procesamiento de lenguaje natural de última generación, LegalBot ayuda a ciudadanos y profesionales a navegar el complejo sistema legal peruano de manera inteligente.

## � Nuevas Funcionalidades Premium

He incorporado las siguientes herramientas avanzadas para llevar la asesoría legal al siguiente nivel:

*   📂 **Analizador de Documentos Propios**: Sube cualquier PDF legal (contratos, notificaciones, cartas) y la IA lo analizará en tiempo real utilizando el contexto del documento para darte respuestas personalizadas.
*   ⚖️ **Modo Simulación de Audiencia**: Activa el rol de **Juez** para practicar antes de una diligencia real. La IA te interrogará y pondrá a prueba tus argumentos legales basándose en la jurisprudencia peruana.
*   🧠 **Razonamiento Few-Shot y CoT**: Mejora drástica en la precisión legal mediante técnicas de "Chain-of-Thought", permitiendo que la IA identifique leyes y artículos específicos antes de dar una conclusión.

## ✨ Características Principales

- 💬 **Chat Inteligente** - Consultas legales dinámicas con base legal sustraída de normas vigentes.
- 📄 **Generación de Documentos** - Modelos profesionales de contratos y escritos listos para descargar.
- � **Búsqueda Vectorial** - Integración con Pinecone para recuperación precisa de artículos legales.
- � **Seguridad Robusta** - Autenticación JWT y protección de datos sensibles.

## �️ Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| **Frontend** | Next.js 14, Tailwind CSS, Framer Motion, shadcn/ui |
| **Backend** | FastAPI (Python 3.12), SQLAlchemy, Pydantic |
| **Modelos IA** | Groq (Llama 3), Gemini Pro, GPT-4o |
| **Base de Datos** | SQLite (Local/Dev), PostgreSQL (Prod), Pinecone (Vectorial) |

## � Despliegue en GitHub (Guía de Seguridad)

Para subir este proyecto a GitHub **sin exponer tus llaves privadas**, sigue estos pasos:

### 1. Verificar el .gitignore
Asegúrate de que tus archivos `.env` y bases de datos locales no se suban.
```bash
# Ya he configurado un .gitignore en la raíz que protege:
# - Todos los archivos .env
# - Carpetas node_modules y venv
# - Base de datos legalbot.db
```

### 2. Inicializar Git y Subir
```bash
git init
git add .
git commit -m "feat: implement advanced AI features and security"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/LegalBOT.git
git push -u origin main
```

### 3. Configurar en el Servidor (Producción)
En tu servicio de hosting (Render, Vercel, DigitalOcean), nunca subas el `.env`. En su lugar, configura las **Environment Variables** en el panel de control del proveedor usando los nombres definidos en `backend/.env.example`.

## ⚙️ Configuración Local

### Requisitos
- Node.js 18+
- Python 3.12+

### Pasos
1. **Clonar el repo**: `git clone ...`
2. **Backend**:
   - `cd backend`
   - `pip install -r requirements.txt`
   - `cp .env.example .env` (y pon tus llaves)
   - `uvicorn app.main:app --reload`
3. **Frontend**:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

---
Desarrollado con ❤️ para transformar el acceso legal en el Perú.
