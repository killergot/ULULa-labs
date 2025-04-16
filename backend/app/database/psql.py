from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import load_config
import os

config = load_config()

# URL подключения к БД, например для PostgreSQL:
# DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/dbname')
DATABASE_URL = (f'postgresql://{config.database.DB_USER}'
                f':{config.database.DB_PASS}@'
                f'{config.database.DB_HOST}/'
                f'{config.database.DB_NAME}')

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
