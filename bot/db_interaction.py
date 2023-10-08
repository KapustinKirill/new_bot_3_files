from models.models import BotUser, BotFile, BotUserFileInteraction
from models import SessionLocal
from sqlalchemy.orm import Session


def get_user_by_telegram_id(telegram_id: int, db: Session):
    return db.query(BotUser).filter(BotUser.telegram_id == telegram_id).first()

def create_user(telegram_id: int, name: str, db: Session):
    user = BotUser(telegram_id=telegram_id, name=name, current_state="START")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_state(user: BotUser, new_state: str, db: Session):
    user.current_state = new_state
    db.commit()
    db.refresh(user)
    return user

def get_all_files(db: Session):
    return db.query(BotFile).all()

# def log_user_file_interaction(user_id: int, file_name: int, delivery_method: str, db: Session):
#     interaction = BotUserFileInteraction(user_id=user_id, file_name=file_name, delivery_method=delivery_method)
def get_user_by_telegram_id(telegram_id: int, db: Session):
    return db.query(BotUser).filter(BotUser.telegram_id == telegram_id).first()

def log_user_file_interaction(user_id: int, file_id: int, delivery_method: str, db: Session):
    id_ = get_user_by_telegram_id(user_id,db)
    interaction = BotUserFileInteraction(user_id=id_.id, file_id=file_id, delivery_method=delivery_method)

    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction

# ... другие функции для работы с БД по мере необходимости ...
from contextlib import contextmanager
from models import SessionLocal

@contextmanager
def db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
