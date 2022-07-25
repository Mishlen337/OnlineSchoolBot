from aiogram import Dispatcher
from loguru import logger
# from core.filters.employee_filters import BoundFilter


def setup(dp: Dispatcher):
    "Setups handlers for employee."
    logger.debug("Start employee's handlers registration.")
    logger.debug("End employee's handlers registration.")