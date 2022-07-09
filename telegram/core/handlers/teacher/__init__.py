"""Package to declare teacher's handlers."""
from aiogram import Dispatcher
from loguru import logger


def setup(dp: Dispatcher):
    "Setups handlers for teacher."
    logger.debug("Start teacher's handlers registration.")
    logger.debug("End teacher's handlers registration.")
