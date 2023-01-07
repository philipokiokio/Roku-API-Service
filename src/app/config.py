from pydantic import BaseSettings



class DatabaseSettings(BaseSettings):
    dbname:str
    dbuser:str
    dbpassword:str
    dbtype:str
    dbhost:str
    dbport:int
    
    
    class Config:
        env_file = ".env"
        


db_settings = DatabaseSettings()