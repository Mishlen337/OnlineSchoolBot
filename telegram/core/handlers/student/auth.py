from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from . import basket
from db.student import user
from db.utils import exceptions
from core.keyboards import student_keyboards


async def precheckout_basket(message: types.Message, state: FSMContext):
    logger.debug(f"Student {message.from_user} in pre-checkout handler")
    user_info = await user.get_user_info(message.from_user.id)
    if not user_info["telephone"] or not user_info["name"]:
        logger.debug(f"Student {message.from_user} is unauthorized")
        await message.answer(
            "Перед оплатой вам нужно зарегестрироваться в боте. Это нужно сделать всего один раз.")
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Отправить номер телефона",
                                            request_contact=True)
        keyboard.add(button_phone)
        await message.answer(
            "Отправьте номер телефона (кнопка отправки встроена в клавиатуру)",
            reply_markup=keyboard)
        await state.set_state("student_telephone")
    else:
        logger.debug(f"Student {message.from_user} is authorized")
        await basket.get_basket(message, state)


async def get_contact(message: types.Message, state: FSMContext):
    logger.debug(f"Student {message.from_user} shared his phone.")
    try:
        await user.telephone_init(message.from_user.id, message.contact.phone_number)
        await state.set_state("student_fio")
        await message.answer(
            "Введите ваше ФИО через пробел (пример: Иванов Иван Иванович).",
            reply_markup=ReplyKeyboardRemove())
    except exceptions.ConnectionError:
        await message.answer("Упс. Что-то пошло не так")


async def get_contact_error(message: types.Message, state: FSMContext):
    await message.answer(
        "Пожалуста, поделитесь телефоном (нажмите кнопку встроенную в клавиатуру).")


async def get_fio(message: types.Message, state: FSMContext):
    logger.debug(f"Student {message.from_user} shared his fio.")
    try:
        surname, name, patronymic = message.text.split(" ")
        await user.fio_init(message.from_user.id, surname, name, patronymic)
        await state.set_state("student_class_num")
        await message.answer(
            "Введите ваш класс (1..11) или введите <b>окончил</b>, если вы уже окончили школу.",
            parse_mode='HTML'
            )
    except exceptions.ConnectionError:
        await message.answer("Упс. Что-то пошло не так")
    except ValueError:
        await message.answer("Введите ФИО через пробел еще раз (пример: Иванов Иван Иванович).")


async def get_class_num(message: types.Message, state: FSMContext):
    logger.debug(f"Student {message.from_user} shared his class num.")
    if message.text != 'окончил':
        try:
            class_num = int(message.text)
            await user.class_num_init(message.from_user.id, class_num)
        except ValueError:
            await message.answer("Неверный формат.")
            await message.answer(
                "Введите ваш класс (1..11) или введите <b>окончил</b>, если вы уже окончили школу.",
                parse_mode="HTML"
            )
            return
        except exceptions.FormatError:
            await message.answer("Неверный класс.")
            await message.answer(
                "Введите ваш класс (1..11) или введите <b>окончил</b>, если вы уже окончили школу.",
                parse_mode="HTML"
            )
            return
        except exceptions.ConnectionError:
            await message.answer("Упс. Что-то пошло не так")
            return
    await message.answer(
        "Вы успешно авторизировались:)",
        reply_markup=student_keyboards.all_keyboards["menu"]())
    await state.set_state("student_main")
    await basket.get_basket(message, state)
