from pydantic_settings import BaseSettings

from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_URL: str
    db_echo: bool
    secret_key: str
    smtp_username: str
    smtp_password: str
    smtp_server: str
    smtp_port: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Setting()




