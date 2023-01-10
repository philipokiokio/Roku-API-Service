# from app.utils.db_utils import get_db
from src.app.database import SessionLocal
from sqlalchemy.orm import Session


class BaseRepo:
    def __init__(self):
        self.db: Session = SessionLocal()


base_repo = BaseRepo()
