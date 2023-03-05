from sqlalchemy import (
    ARRAY,
    JSON,
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.orm import relationship

from . import AbstractBase


class Campaign(AbstractBase):
    __tablename__ = "campaign"
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    workspace_id = Column(
        Integer,
        ForeignKey("workspace.id", ondelete="DONOTHING"),
    )
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    campaign_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    api_key = Column(String, nullable=False)
    end_of_day_report = Column(Boolean, nullable=False, server_default=text("false"))
    created_by = Column(Integer, ForeignKey("user.id", ondelete="NULL"), nullable=True)
    creator = relationship("User")
    Workspace = relationship("Workspace")


class Event(AbstractBase):
    __tablename__ = "campaign_events"
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    campaign_id = Column(
        Integer, ForeignKey("campaign.id", ondelete="CASCADE"), nullable=False
    )
    has_rewards = Column(Boolean, nullable=False)
    campaign = relationship("Campaign")


class EventRewards(AbstractBase):
    __tablename__ = "event_rewards"
    event_id = Column(Integer, ForeignKey("campaign_events.id", ondelete="CASCADE"))
    rewards = Column(
        MutableList.as_mutable(ARRAY(MutableDict.as_mutable(JSON))), nullable=False
    )
    event = relationship("events")
    pass


class EventRefferal(AbstractBase):
    __tablename__ = "event_refferal"

    campaign_event_id = Column(
        Integer, ForeignKey("campaign_events.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    count = Column(Integer, nullable=False)
    refferal_code = Column(String, nullable=False)
    fraud_flag = Column(Boolean, server_default=text("false"))
    fraud_counter = Column(Integer, nullable=False)
    campaign = relationship("Event")


class Coupon(AbstractBase):
    __tablename__ = "coupons"
    campaign_id = Column(
        Integer, ForeignKey("campaign.id", ondelete="CASCADE"), nullable=False
    )
    slug = Column(String, nullable=False)
    coupon = Column(String, nullable=False)
    value_off = Column(Float, nullable=False)
    count_made = Column(Integer, nullable=False)

    campaign = relationship("Campaign")
