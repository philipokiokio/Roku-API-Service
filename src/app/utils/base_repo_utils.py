# from app.utils.db_utils import get_db
from src.app.database import SessionLocal
from sqlalchemy.orm import Session
from uuid import uuid4


class BaseRepo:
    def __init__(self):
        self.db: Session = SessionLocal()

    def slugger(self, name):
        next = uuid4()
        slug = f"{name}-{next.hex[:10]}"
        return slug


base_repo = BaseRepo()
