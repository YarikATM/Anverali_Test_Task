from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DEBUG: bool
    DB_HOST: str
    DB_USER: SecretStr
    DB_PASSWORD: SecretStr
    DB_NAME: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = Settings()
