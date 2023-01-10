from . import AbstractBase
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date, text
from sqlalchemy.orm import relationship


class Campaign(AbstractBase):
    __tablename__ = "campaign"
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    campaign_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    api_key = Column(String, nullable=False)
    end_of_day_report = Column(Boolean, nullable=False, server_default=text("false"))
    created_by = Column(Integer, ForeignKey("user.id", ondelete="NULL"), nullable=True)
    creator = relationship("User")
    members = relationship("CampaignTeamMember", back_refs="campaign")


class CampaignTeamMember(AbstractBase):
    __tablename__ = "campaign_member"
    campaign_id = Column(
        Integer, ForeignKey("campaign.id", ondelete="CASCADE"), nullable=False
    )
    member_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    role = Column(String, nullable=False)

    member = relationship("User")
    campaign = relationship("Campaign")


class CampaignRefferal(AbstractBase):
    __tablename__ = "campaign_refferal"

    campaign_id = Column(
        Integer, ForeignKey("campaign.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    count = Column(Integer, nullable=False)
    fraud_flag = Column(Boolean, server_default=text("false"))
    campaign = relationship("Campaign")


class CampaignRefEmail(AbstractBase):
    __tablename__ = "campaign_ref_email"
    campaign_id = Column(
        Integer, ForeignKey("campaign.id", ondelete="CASCADE"), nullable=False
    )
    email = Column(String, nullable=False)
    campaign = relationship("Campaign")
