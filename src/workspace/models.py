from src.app.utils.sqlmodels_utils import AbstractBase
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, text

from sqlalchemy.orm import relationship


class Workspace(AbstractBase):
    __tablename__ = "workspace"
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    created_by = Column(
        Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=True
    )
    is_premium = Column(Boolean, server_default=text("false"))
    revoke_link = Column(Boolean, server_default=text("false"))
    creator = relationship("User")
    workspace_member = relationship("WorkspaceMember", backref="member")


class WorkspaceMember(AbstractBase):
    __tablename__ = "workspace_member"
    workspace_id = Column(
        Integer, ForeignKey("workspace.id", ondelete="CASCADE"), nullable=False
    )
    member_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    role = Column(String, nullable=False)

    member = relationship("User")
    workspace = relationship("Workspace")
