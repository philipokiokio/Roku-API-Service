from pydantic import BaseModel
from enum import Enum


class AbstractModel(BaseModel):
    class Config:
        orm_mode = True
        use_enum_values = True


class ResponseModel(AbstractModel):
    message: str
    status: int


class CampaignType(Enum):
    sign_up = "SignUp"
    event = "Event"


class CampaignStatus(Enum):
    on_going = "On Going"
    completed = "Completed"


class RoleOptions(Enum):
    member = "Member"
    guest = "Guest"
    admin = "Admin"


class User(AbstractModel):
    id: int
    first_name: str
    last_name: str
    email: str
