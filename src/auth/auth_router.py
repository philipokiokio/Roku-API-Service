from fastapi import APIRouter, status, Depends
from src.auth import schemas
from src.auth.auth_service import user_service
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

user_router= APIRouter(prefix="/api/v1/auth", tags={"User Authentication"})


@user_router.post("/register/", status_code=status.HTTP_201_CREATED, response_model=schemas.MessageUserResponse)
def register(user_create:schemas.user_create):
    
    new_user= user_service.register(user_create)
    return {
        "message": "Registration Sucessful",
        "data": new_user,
        "status": status.HTTP_201_CREATED
    }    
    
@user_router.post("/login/", status_code=status.HTTP_200_OK, response_model=schemas.MessageLoginResponse)
def login(login_user:OAuth2PasswordRequestForm= Depends()):
    user_login = user_service.login(login_user)
    return {
        "message": "Login Successful",
        "data": user_login,
        "status": status.HTTP_200_OK
    }
    