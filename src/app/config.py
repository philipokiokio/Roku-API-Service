from pydantic import BaseSettings, EmailStr


class UtilSettingsMixin(BaseSettings):
    class Config:
        env_file = ".env"


class DatabaseSettings(UtilSettingsMixin):
    dbname: str
    dbuser: str
    dbpassword: str
    dbtype: str
    dbhost: str
    dbport: int


class AuthSettings(UtilSettingsMixin):
    access_secret_key: str
    algorithm: str
    access_time_exp: int
    refresh_secret_key: str
    refresh_time_exp: int


class MailSettings(UtilSettingsMixin):
    mail_username: str
    mail_password: str
    mail_from: EmailStr
    mail_port: int
    mail_server: str
    mail_from_name: str


auth_settings = AuthSettings()
db_settings = DatabaseSettings()
mail_settings = MailSettings()
