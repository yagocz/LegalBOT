import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import sys

# La URL que proporcionaste (ajustada internamente para asyncpg)
DATABASE_URL = "postgresql+asyncpg://postgres:lamineyamal@db.zwqzewnkyaouvzcwwsvq.supabase.co:5432/postgres"

async def test_supabase_connection():
    print("🚀 Probando conexión con Supabase...")
    try:
        engine = create_async_engine(DATABASE_URL)
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version();"))
            row = result.fetchone()
            print(f"✅ ¡ÉXITO! Conectado a Supabase.")
            print(f"📦 Versión de DB: {row[0]}")
        await engine.dispose()
    except Exception as e:
        print(f"❌ ERROR de conexión: {e}")
        print("\nPosibles causas:")
        print("1. Revisa si la contraseña 'lamineyamal' es correcta.")
        print("2. Asegúrate de que Supabase permite conexiones externas (Network Restrictions).")
        print("3. Revisa que no haya espacios en blanco en la URL.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_supabase_connection())
