from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from . import AbstractBase


class User(AbstractBase):
    __tablename__ = "users"
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable= False)
    email = Column(String, unique=True)
    password = Column(String, nullable= False)
    
    
class RefreshToken(AbstractBase):
    __tablename__ = "user_refresh_token"
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable= False)
    token = Column(String, nullable= False)
    user = relationship("User")

