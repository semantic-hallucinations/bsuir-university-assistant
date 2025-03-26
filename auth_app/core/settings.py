from pydantic_settings import BaseSettings, SettingsConfigDict
import os 

class AuthSettings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_HOST: str
    DB_PORT: str
    DB_PASSWORD: str

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.env"), extra="ignore")

    def db_connection_url(self):
        return f"postresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
auth_settings = AuthSettings()