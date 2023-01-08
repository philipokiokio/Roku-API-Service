from src.app.config import auth_settings
from jose import JWTError,jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException, Header
from app.utils.db_utils import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .schemas import TokenData
from .models import User, RefreshToken


oauth_schemes = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")



access_secret_key = auth_settings.access_secret_key
refresh_secret_key = auth_settings.refresh_secret_key
access_time_exp = auth_settings.access_time_exp
refresh_time_exp = auth_settings.refresh_time_exp
algorithm = auth_settings.algorithm





def create_access_token(data:dict)->str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes = access_time_exp)
    to_encode = to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode,access_secret_key, algorithm=algorithm)
    return encode_jwt

    

def create_refresh_token(data:dict)->str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes = refresh_time_exp)
    to_encode = to_encode.update({"exp": expire})
    refresh_encode_jwt = jwt.encode(to_encode,refresh_secret_key, algorithm=algorithm)
    return refresh_encode_jwt




def credential_exception():
    
    raise HTTPException(
        detail="Could not validate credentials",
        status_code= status.HTTP_401_UNAUTHORIZED,
        headers= {"WWW-Authenticate": "Bearer"}
    )
    
    
def refresh_exception():
    
    raise HTTPException(
        detail="Could not validate refresh credential",
        status_code= status.HTTP_400_BAD_REQUEST,
        headers= {"Refresh-Tok": "token"}
    )
    
    
    
def verify_refresh_token(refresh_tok:str = Header(), db:Session = Depends(get_db))->str:
    
    try: 
        decoded_data = jwt.decode(refresh_tok, refresh_secret_key, algorithms=[algorithm])
        email = decoded_data.get("email")
        if not email:
            raise refresh_exception()
        token_data = TokenData(email=email)
    except JWTError:
        raise refresh_exception()

    refresh_token_check = db.query(
        RefreshToken
    ).filter(
        RefreshToken.token == refresh_tok
    ).first()
    
    if not refresh_token_check:
        refresh_exception()
    
    if refresh_token_check.user.email != token_data.email:
        refresh_exception()
        
    return create_access_token(decoded_data)
      
    
    
    
    
        
    
    
def get_current_user(token:str = Depends(oauth_schemes),db:Session = Depends(get_db)):
    
    try:
        decode_data= jwt.decode(token, access_secret_key, algorithms=[algorithm])
        email = decode_data.get("email")
        if email is None:
            credential_exception()
            
        token_data = TokenData(email= email)
        
        
    except JWTError:
        credential_exception()
    
    user_check = db.query(User).filter(User.email == token_data.email).first()
    if not user_check:
        credential_exception()
    
    
    return user_check