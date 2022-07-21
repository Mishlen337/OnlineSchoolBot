"""Module to declare basic variables."""
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pydantic import BaseSettings


class Settings(BaseSettings):
    WEBHOOK_URL: str
    TELEGRAM_SECRET: str
    PAYMENTS_SECRET: str

    class Config:
        env_file = "../.env"


config = Settings()

storage = MemoryStorage()
bot = Bot(token=config.TELEGRAM_SECRET)
dp = Dispatcher(bot, storage=storage)
