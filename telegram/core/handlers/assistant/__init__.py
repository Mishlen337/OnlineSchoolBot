"""Package to declare assistant's handlers."""
from aiogram import Dispatcher
from loguru import logger


def setup(dp: Dispatcher):
    "Setups handlers for assistant."
    logger.debug("Start assistant's handlers registration.")
    logger.debug("End assistant's handlers registration.")
