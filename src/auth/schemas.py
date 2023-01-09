from pydantic import BaseModel, EmailStr
from datetime import datetime


class TokenData(BaseModel):
    email:EmailStr
    
    
class user_create(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    password:str
    
    
    
class UserResponse(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    date_created:datetime
    
    class Config:
        orm_mode= True
    
class MessageUserResponse(BaseModel):
    message:str
    data:UserResponse
    status:int
    
class Token(BaseModel):
    token:str 
    
        
class AccessToken(Token):
    type:str
    
class RefreshToken(Token):
    header:str


class LoginResponse(BaseModel):
    data: UserResponse
    access_token: AccessToken
    refresh_token: RefreshToken
    
    class Config:
        orm_mode=True
        
class MessageLoginResponse(BaseModel):
    message:str
    data: LoginResponse
    status:int
    
    