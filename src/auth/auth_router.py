from fastapi import APIRouter, status, Depends
from src.auth import schemas
from src.auth.auth_service import user_service
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.auth.oauth import get_current_user, verify_refresh_token

user_router = APIRouter(prefix="/api/v1/auth", tags={"User Authentication"})


@user_router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MessageUserResponse,
)
def register(user_create: schemas.user_create):

    new_user = user_service.register(user_create)
    return {
        "message": "Registration Sucessful",
        "data": new_user,
        "status": status.HTTP_201_CREATED,
    }


@user_router.post(
    "/login/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageLoginResponse,
)
def login(login_user: OAuth2PasswordRequestForm = Depends()):
    user_login = user_service.login(login_user)
    return {
        "message": "Login Successful",
        "data": user_login,
        "status": status.HTTP_200_OK,
    }


@user_router.get(
    "/me/", status_code=status.HTTP_200_OK, response_model=schemas.MessageUserResponse
)
def logged_in_user(current_user: dict = Depends(get_current_user)):

    return {"message": "Me Data", "data": current_user, "status": status.HTTP_200_OK}


@user_router.patch(
    "/update/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageUserResponse,
)
def update_user(
    update_user: schemas.UserUpdate, current_user: dict = Depends(get_current_user)
):

    update_user = user_service.update_user(update_user, current_user)

    return {
        "message": "User Updated Successfully",
        "data": update_user,
        "status": status.HTTP_200_OK,
    }


@user_router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(current_user: dict = Depends(get_current_user)):

    user_service.delete(current_user)
    return {"status": status.HTTP_204_NO_CONTENT}


@user_router.get("/refresh/", status_code=status.HTTP_200_OK)
def get_new_token(new_access_token: str = Depends(verify_refresh_token)):

    return {
        "message": "New access token created successfully",
        "token": new_access_token,
        "status": status.HTTP_200_OK,
    }
