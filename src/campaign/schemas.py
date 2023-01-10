from src.app.utils.base_schemas import (
    AbstractModel,
    CampaignType,
    CampaignStatus,
    RoleOptions,
    User,
    ResponseModel,
)
from datetime import date, datetime
from typing import Optional, List
from pydantic import EmailStr


class CampaignCreate(AbstractModel):
    name: str
    start_date: date
    end_date: date | None
    campaign_type: CampaignType
    status: CampaignStatus
    end_of_day_report: Optional[bool]


class CampaignUpdate(AbstractModel):
    name: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    campaign_type: Optional[CampaignType]
    status: Optional[CampaignStatus]
    end_of_day_report: Optional[bool]


class CampaignMember(User):
    pass


class CampaignRepsonse(CampaignCreate):
    id: int
    slug: str
    created_by: User
    api_key: str
    members: List[CampaignMember]
    date_created: datetime


class CampaignORMResp(AbstractModel):
    name: str
    slug: str


class MessageCampaignResponse(ResponseModel):
    data: CampaignRepsonse


class MessageListCampaignResponse(ResponseModel):
    data: List[CampaignRepsonse]


class SendCampaignInvite(AbstractModel):
    email: EmailStr
    role: RoleOptions


class UpdateRole(AbstractModel):
    role: RoleOptions


class CampaignTeamMemberResponse(User):
    campaign: CampaignORMResp


class MessageCampaignTeamResp(ResponseModel):
    data: CampaignTeamMemberResponse


class MessageListCampaignTeamResp(ResponseModel):
    data: List[CampaignTeamMemberResponse]
