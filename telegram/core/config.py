"""Module to declare basic variables."""
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from pydantic import BaseSettings


class Settings(BaseSettings):
    WEBHOOK_URL: str
    TELEGRAM_SECRET: str
    PAYMENTS_SECRET: str
    TG_HOST: str
    HOST_PORT: int
    MODERATOR_TG_ID: int
    TERMS_PATH: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: int
    REDIS_PASSWORD: str

    class Config:
        env_file = "../.env"


config = Settings()

storage = RedisStorage2(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB, config.REDIS_PASSWORD)
bot = Bot(token=config.TELEGRAM_SECRET)
dp = Dispatcher(bot, storage=storage)
