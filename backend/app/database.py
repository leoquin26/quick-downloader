import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Carga variables de entorno desde el .env (solo útil en local)
load_dotenv()

# Obtiene URI y nombre de la base de datos desde el entorno
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "quick_downloader_db")

# Validación mínima (opcional pero recomendable)
if not MONGO_URI:
    raise ValueError("MONGO_URI not set in environment variables")

# Conexión al cliente y base de datos
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
