from typing import Optional
import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_HOST: str = Field("0.0.0.0", env="API_HOST")
    API_PORT: int = Field(8000, env="API_PORT")
    API_SECRET_KEY: str = Field("dev-secret-key", env="API_SECRET_KEY")
    API_ENVIRONMENT: str = Field("development", env="API_ENVIRONMENT")
    
    # LLM Configuration
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")
    GOOGLE_API_KEY: Optional[str] = Field(None, env="GOOGLE_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    
    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    AUTH_ENABLED: bool = Field(False, env="AUTH_ENABLED")
    
    # Logging
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @property
    def is_development(self) -> bool:
        """Check if environment is development."""
        return self.API_ENVIRONMENT.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if environment is production."""
        return self.API_ENVIRONMENT.lower() == "production"
    
    @property
    def is_testing(self) -> bool:
        """Check if environment is testing."""
        return self.API_ENVIRONMENT.lower() == "testing"


# Create settings instance
settings = Settings()
