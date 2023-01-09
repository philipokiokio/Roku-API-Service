from src.auth.auth_repository import user_repo,token_repo
from fastapi import HTTPException, status
from src.auth import schemas
from src.auth.models import User, RefreshToken
from src.app.utils.db_utils import hash_password, verify_password
from src.auth.oauth import credential_exception, create_refresh_token,create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder





class UserService:
    
    
    def __init__(self):
        self.user_repo = user_repo
        self.token_repo = token_repo
    
    def register(self,user:schemas.user_create)->User:
        
        user_check = self.user_repo.get_user(user.email)
        if user_check:
            raise HTTPException(detail="This User has an account", status_code= status.HTTP_400_BAD_REQUEST)
        user.password = hash_password(user.password)
        return self.user_repo.create(user)
    
    def login(self,user:OAuth2PasswordRequestForm)->schemas.LoginResponse:
        user_check = self.user_repo.get_user(user.username)
        if not user_check:
            raise HTTPException(detail="User does not exist", status_code=status.HTTP_400_BAD_REQUEST)
        
        pass_hash_check = verify_password(user_check.password, user.password)
        if not pass_hash_check:
            credential_exception()
        
        
        
        access_token= create_access_token(jsonable_encoder(user_check))
        refresh_token = create_refresh_token(jsonable_encoder(user_check))
        
        token_check = self.token_repo.get_token(user_check.id)
        if token_check:
            token_check.token = refresh_token
            self.token_repo.update_token(token_check)
        else:
            self.token_repo.create_token(refresh_token, user_check.id)
            
            
            
        access_token_ = {
            "token": access_token,
            "type": "Bearer"
        }
        refresh_token_ = {
            "token": refresh_token,
            "header":"Refresh-Tok"
        }
        login_resp = schemas.LoginResponse(data=user_check, access_token= access_token_, refresh_token=refresh_token_)
        return login_resp
        
user_service = UserService()        