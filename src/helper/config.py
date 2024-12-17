from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):

    #base.py / route
    APP_NAME:str
    APP_VERSION:str
    OPENAI_API_KEY:str

    # data.py Upload route
    FILE_ALLOWED_TYPE :str
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNK_SIZE:int

    MONGODB_URL:str
    MONGODB_DATABASE:str

    class Config:
        env_file=".env"

def get_settings():
    return Settings()
