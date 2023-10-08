from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class BotUser(Base):
    __tablename__ = 'bot_users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    name = Column(String, nullable=False)
    email = Column(String)
    current_state = Column(String, nullable=False)
    interactions = relationship("BotUserFileInteraction", back_populates="user")

class BotFile(Base):
    __tablename__ = 'bot_files'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)


class BotUserFileInteraction(Base):
    __tablename__ = 'bot_user_file_interactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('bot_users.id'))
    file_id = Column(Integer, ForeignKey('bot_files.id'))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    delivery_method = Column(String, nullable=False)

    user = relationship("BotUser", back_populates="interactions")
    file = relationship("BotFile")


