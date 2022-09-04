from aiogram import Dispatcher
from loguru import logger

from . import auth, personal_schedule, homework
# from core.filters.employee_filters import BoundFilter


def setup(dp: Dispatcher):
    "Setups handlers for employee."
    logger.debug("Start employee's handlers registration.")
    dp.register_message_handler(auth.get_contact,
                                content_types="contact",
                                state="employee_telephone")
    dp.register_message_handler(auth.get_contact_error,
                                state="employee_telephone")
    dp.register_message_handler(personal_schedule.get_schedule,
                                state="employee_main", regexp="Занятия")
    dp.register_message_handler(homework.get_homeworks,
                                state="employee_main", regexp="Проверка дз")
    logger.debug("End employee's handlers registration.")
