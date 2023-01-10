from sqlalchemy import Column, Integer, TIMESTAMP, text
from src.app.database import Base


class AbstractBase(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    date_created = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    date_updated = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
