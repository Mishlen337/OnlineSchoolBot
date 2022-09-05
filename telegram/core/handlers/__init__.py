"""Package to declare all handlers."""
from aiogram import Dispatcher
from loguru import logger
from .start_handler import base_handler, commands_handler
from . import student, employee, moderator


def setup(dp: Dispatcher):
    "Setups all handlers."
    logger.debug("Start base handler registration.")
    dp.register_message_handler(commands_handler,
                                commands=["start", "stop", "help", "getlink", "terms"], state="*")
    student.setup(dp)
    employee.setup(dp)
    moderator.setup(dp)
    dp.register_message_handler(base_handler, state="*")
    logger.debug("End base handler registration.")
