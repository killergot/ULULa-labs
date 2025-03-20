from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL подключения к БД, например для PostgreSQL:
# DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')
DATABASE_URL = 'postgresql://postgres:132435@localhost:5432/ulula'

# Создаем объект движка (engine) для SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
