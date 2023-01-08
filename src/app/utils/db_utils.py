from src.app.database import SessionLocal
from passlib.context import CryptContext



def get_db():
    db = SessionLocal()
    
    try: 
        yield db
    except:
        db.rollback()
    finally:
        db.close()
        
        
        
        
pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")        


def hash_password(password:str)->str:
    return pwd_context.hash(password)


def verify_password(hashed_password:str, raw_password)->bool:
    return pwd_context.verify(raw_password, hashed_password)    