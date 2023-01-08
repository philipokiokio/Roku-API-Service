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
        



class AuthSettings(BaseSettings):
    access_secret_key:str
    algorithm:str
    access_time_exp:int
    refresh_secret_key:str
    refresh_time_exp:int
    
    
    class Config:
        env_file = ".env"
        
        















auth_settings = AuthSettings()
db_settings = DatabaseSettings()