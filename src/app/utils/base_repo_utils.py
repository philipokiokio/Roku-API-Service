# from app.utils.db_utils import get_db
from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from src.app.database import SessionLocal


class BaseRepo:
    def __init__(self):
        self.db: Session = self.get_db.__next__()

    @property
    def get_db(self):
        session = SessionLocal()
        try:
            yield session
        except:
            session.rollback()
        finally:
            session.close()
        SessionLocal.remove()

    def slugger(self, name):
        next = uuid4()
        slug = f"{name}-{next.hex[:10]}"
        return slug

    @property
    def time_slugger(self):

        today = datetime.now()
        today = str(int(datetime.timestamp(today) * 1000))[0:8]
        random_ids = uuid4()
        slug = f"{today}-{random_ids.hex[:8]}"
        return slug


class BaseActionMixinRepo(BaseRepo):
    def __init__(self, model):
        self.model = model
        super().__init__()

    @property
    def base_query(self):
        return self.db.query(self.model)

    def create(self, create_dict: dict):
        new_data = self.model(**create_dict)
        self.db.add(new_data)
        self.db.commit()
        self.db.refresh(new_data)
        return new_data

    def update(self, data):
        self.db.commit()
        self.db.refresh(data)
        return data

    def delete(self, data):
        self.db.delete(data)
        self.db.commit()
