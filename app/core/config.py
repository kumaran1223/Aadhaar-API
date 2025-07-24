import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    app_name: str = "Aadhaar OCR API"
    app_version: str = "1.0.0"
    debug: bool = True

    # Supabase Configuration
    supabase_url: str = ""
    supabase_key: str = ""

    # CORS Configuration
    allowed_origins: str = "http://localhost:3000,http://localhost:8080,http://127.0.0.1:8000"

    class Config:
        env_file = ".env"

    def get_allowed_origins(self) -> List[str]:
        """Parse allowed origins from string to list"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]

settings = Settings()
