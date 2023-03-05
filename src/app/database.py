from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from src.app.config import db_settings

SQLALCHEMY_DB_URL = f"{db_settings.dbtype}://{db_settings.dbuser}:{db_settings.dbpassword}@{db_settings.dbhost}:{db_settings.dbport}/{db_settings.dbname}"

engine = create_engine(SQLALCHEMY_DB_URL)


SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


SessionLocal = scoped_session(SessionFactory)
Base = declarative_base()

print("Database is ready!")
