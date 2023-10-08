from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
from models.postgres_storage import PostgresStorage

# Создаем объект engine для подключения к БД
engine = create_engine(config.DATABASE_URL)

# Создаем класс Session, который будет использоваться для создания объектов Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
