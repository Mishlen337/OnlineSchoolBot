from aiogram import Dispatcher
from loguru import logger

from . import auth
# from core.filters.employee_filters import BoundFilter


def setup(dp: Dispatcher):
    "Setups handlers for employee."
    logger.debug("Start employee's handlers registration.")
    dp.register_message_handler(auth.get_contact,
                                content_types="contact",
                                state="employee_telephone")
    dp.register_message_handler(auth.get_contact_error,
                                state="employee_telephone")
    logger.debug("End employee's handlers registration.")
