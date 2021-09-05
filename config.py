import os

from pydantic import BaseSettings


class Config(BaseSettings):
    secret_key: bytes


env_file = os.getenv("ENV_FILE", ".env")
config = Config(_env_file=env_file, _env_file_encoding="utf-8")
