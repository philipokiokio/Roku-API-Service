from src.app.database import SessionLocal




def get_db():
    db = SessionLocal()
    
    try: 
        yield db
    except:
        db.rollback()
    finally:
        db.close()