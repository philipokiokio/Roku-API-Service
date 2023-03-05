from datetime import date, datetime
from typing import Dict, List, Optional

from pydantic import EmailStr

from src.app.utils.base_schemas import (
    AbstractModel,
    CampaignStatus,
    CampaignType,
    ResponseModel,
    User,
)


# Campaign DTO's
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


# Event DTO's
class EventCreate(AbstractModel):
    name: str


class EventResp(AbstractModel):
    id: int
    name: str
    campaign: CampaignORMResp
    refferal_data: Optional[Dict[str, int]]


class MessageEventResp(ResponseModel):
    data: EventResp


class MessageEventResp(ResponseModel):
    data: List[EventResp]


# Event Refferal DTO
class EventRefCreate(AbstractModel):
    name: str
    email: str


class EventRefResp(AbstractModel):
    id: int
    name: str
    email: str
    count: int
    refferal_code: str
    fraud_counter: int
    fraud_flag: bool
    event: CampaignORMResp


class MessageEventResp(ResponseModel):
    data: EventRefResp


class MessageListEventResp(ResponseModel):
    data: List[EventRefResp]


# coupon DTO's


class CouponCreate(AbstractModel):
    coupon: str
    value_off: float


class CouponResp(AbstractModel):
    id: int
    coupon: str
    value_off: float
    count_made: int
    campaign: CampaignORMResp


class MessageCouponResp(ResponseModel):
    data: CouponResp


class MessageListCouponResp(ResponseModel):
    data: List[CouponResp]


# Rewards DTO's


class TieredRewards(AbstractModel):
    tier_count: int
    reward: str


class RewardCreate(AbstractModel):
    rewards = List[TieredRewards]


class RewardResp(AbstractModel):
    id: int
    event: CampaignORMResp


class MessageRewardResp(ResponseModel):
    data: RewardResp


class MessageRewardListResp(ResponseModel):
    data: List[RewardResp]
