from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Negi UMS API"
    admin_email: str = "namanegippoi@gmail.com"
    items_per_user: int = 50
    jwt_secret_key: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()