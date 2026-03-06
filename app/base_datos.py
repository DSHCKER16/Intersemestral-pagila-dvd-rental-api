from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.configuracion import obtener_configuracion

config = obtener_configuracion()

engine = create_engine(
    config.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def obtener_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
import os
from contextlib import contextmanager
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

load_dotenv()

DB_URI = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/pagila")
if "+psycopg2" in DB_URI:
    DB_URI = DB_URI.replace("+psycopg2", "+psycopg")

engine = create_engine(DB_URI, echo=False, pool_pre_ping=True, isolation_level="READ COMMITTED", future=True)

@contextmanager
def get_connection() -> Generator[Connection, None, None]:
    with engine.connect() as conn:
        yield conn