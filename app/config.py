from pydantic import BaseConfig
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


_baseConfig  = SettingsConfigDict( 
        env_file=BASE_DIR / ".env",
        env_ignore_empty=True,
        extra="ignore",
    ) 
class DataBaseSetting(BaseSettings):

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT : int

    model_config = _baseConfig

    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

class SecuritySettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_TOKEN_EXPIRE: int
    
    model_config = _baseConfig 


db_settings = DataBaseSetting()  # type: ignore
db_settings.POSTGRES_URL
security_settings = SecuritySettings()  # type: ignore


