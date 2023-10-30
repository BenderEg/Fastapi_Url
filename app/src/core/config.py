from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../../.env',
                                      env_file_encoding='utf-8',
                                      extra='ignore')
    redis_host: str
    redis_port: int
    redis_db: int
    domain: str
    cache: int = 3600

settings = Settings()