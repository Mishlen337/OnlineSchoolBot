from loguru import logger
from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from db.utils import exceptions
from db.employee.auth import auth_employee
from core.keyboards import employee_keyboards


async def get_contact(message: types.Message, state: FSMContext):
    logger.debug(f"Employee {message.from_user} shared his phone {message.contact.phone_number}.")
    try:
        await auth_employee(message.from_user.id, message.contact.phone_number)
        await state.set_state("employee_main")
        await message.answer("Вы успешно зарегистрировались:)",
                             reply_markup=employee_keyboards.all_keyboards["menu"]())
    except exceptions.AuthError:
        await message.answer(
            "Данного номера нет в базе сотрудника. Нажмите еще раз /start, чтобы войти в качестве гостя.")
        await state.reset_state()
    except exceptions.ConnectionError:
        await message.answer("Упс. Что-то пошло не так")


async def get_contact_error(message: types.Message, state: FSMContext):
    await message.answer(
        "Пожалуста, поделитесь телефоном (нажмите кнопку встроенную в клавиатуру).")
