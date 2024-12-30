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

    GENERATION_BACKEND:str
    EMBEDDING_BACKEND:str

    OPENAI_API_KEY:str=None
    OPENAI_API_URL:str=None
    COHERE_API_KEY:str=None

    GENERATION_MODEL_ID:str=None
    EMBEDDING_MODEL_ID:str=None
    EMBEDDING_MODEL_SIZE:str=None

    INPUT_DEFAULT_MAX_CHARACTERS:str=None
    GENERATION_DEFAULT_OUTPUT_TOKENS:str=None
    GENERATION_DEFAULT_TEMPERATURE:str=None

    VECTOR_DB_BAKEND:str
    VECTOR_DB_PATH:str
    VECTOR_DB_DISTANCE_METHOD:str=None
    class Config:
        env_file=".env"

def get_settings():
    return Settings()
