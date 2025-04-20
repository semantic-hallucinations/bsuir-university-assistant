from pydantic_settings import BaseSettings, SettingsConfigDict
import os 

class ModelSettings(BaseSettings):
    MODEL_NAME: str
    API_CLIENT_TOKEN: str

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.env"), extra="ignore")

    def get_model_name(self):
        return self.MODEL_NAME
    
    def get_model_key(self):
        return self.API_CLIENT_TOKEN
    
settings = ModelSettings()
