"""Package to declare moderator's handlers."""
from aiogram import Dispatcher
from loguru import logger


def setup(dp: Dispatcher):
    "Setups handlers for moderator."
    logger.debug("Start moderator's handlers registration.")
    logger.debug("End moderator's handlers registration.")
