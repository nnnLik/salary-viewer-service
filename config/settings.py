from pydantic import BaseSettings
from dotenv import dotenv_values


class ServerSettings(BaseSettings):
    HOST: str
    PORT: int
    SECRET: str


class DatabaseSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str


class Settings(BaseSettings):
    server: ServerSettings = ServerSettings()
    database: DatabaseSettings = DatabaseSettings()


def load_settings() -> Settings:
    env_file = ".env.server"
    env_values = dotenv_values(env_file)

    settings = Settings()

    settings.server.HOST = env_values.get("HOST")
    settings.server.PORT = int(env_values.get("PORT"))
    settings.server.SECRET = env_values.get("SECRET")

    settings.database.DB_HOST = env_values.get("DB_HOST")
    settings.database.DB_PORT = int(env_values.get("DB_PORT"))
    settings.database.DB_NAME = env_values.get("DB_NAME")
    settings.database.DB_USER = env_values.get("DB_USER")
    settings.database.DB_PASS = env_values.get("DB_PASS")

    return settings


settings = load_settings()
