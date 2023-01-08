from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    email:EmailStr