from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Code Assistant & Productivity Bot"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api"
    
    # Add your OpenAI API key in .env file
    OPENAI_API_KEY: str = Field(default="")
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./code_assistant.db"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings() 