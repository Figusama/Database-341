import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Copy .env.example to .env and fill it in.")

def _default_driver() -> str:
    try:
        import psycopg2
        return "psycopg2"
    except ImportError:
        return "pg8000"

for prefix in ("postgres://", "postgresql://"):
    if DATABASE_URL.startswith(prefix):
        DATABASE_URL = f"postgresql+{_default_driver()}://" + DATABASE_URL[len(prefix):]

connect_args = {}
if "supabase.co" in DATABASE_URL or "supabase.com" in DATABASE_URL:
    if DATABASE_URL.startswith("postgresql+pg8000://"):
        import ssl
        connect_args["ssl_context"] = ssl.create_default_context()
    else:
        connect_args["sslmode"] = "require"

engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("SQL_ECHO", "true").lower() == "true",
    pool_size=5,
    max_overflow=5,
    pool_timeout=40,
    pool_recycle=1800,
    pool_pre_ping=True,
    connect_args=connect_args
)

def get_session():
    with Session(engine) as session:
        yield session