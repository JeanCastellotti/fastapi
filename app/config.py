from pydantic import BaseSettings


# Settings
class Settings(BaseSettings):
    database_uri: str
    jwt_secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
