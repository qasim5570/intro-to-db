import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pymongo import MongoClient

load_dotenv()

# --- Test Postgres ---
try:
    engine = create_engine(os.getenv("DATABASE_URL"))
    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_database();"))
        db_name = result.scalar()
        print(f"✅ Postgres connected. Current database: {db_name}")
except Exception as e:
    print(f"❌ Postgres connection failed: {e}")

# --- Test MongoDB ---
try:
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("MONGO_DB_NAME")]
    collections = db.list_collection_names()
    print(f"✅ MongoDB connected. Collections found: {collections}")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
