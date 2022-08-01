"""Module to declare handlers related with courses."""
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext

from core.keyboards.student_keyboards import all_keyboards
from db.student import course
from db.utils import exceptions


async def get_courses(message: types.Message, state: FSMContext):
    """Answers available courses."""
    logger.debug(f"Student {message.from_user} requests available courses.")
    try:
        course_list = await course.get_courses(message.from_user.id)
    except exceptions.ConnectionError:
        await message.answer("Упс. Что то пошло не так")
        return

    num_of_courses = len(course_list)
    if num_of_courses > 0:
        await message.answer("Сообщение о скидке.")
        for crs in course_list:
            info_course = (f"{crs['name_course']}\n"
                           f"{crs['name_subject']}\n"
                           f"{crs['name_teacher']}\n"
                           f"{crs['price_course']}\n")
            if crs['Basket']:
                await message.answer(f"{info_course}Курс находится в корзине", parse_mode="HTML",
                                     reply_markup=all_keyboards["course_desc"]())
            elif crs['Selected']:
                await message.answer(f"{info_course}Курс уже выбран", parse_mode="HTML",
                                     reply_markup=all_keyboards["course_desc"]())
            else:
                await message.answer(f"{info_course}", parse_mode="HTML",
                                     reply_markup=all_keyboards["course_select_with_desc"]())
    else:
        await message.answer("Курсы отсутствуют.")


async def callback_desc(call: types.CallbackQuery):
    # TODO task is to send teacher questionnaires (or links to them)
    text = call.message.text
    if (text.find('Курс находится в корзине') != -1) or ((text.find('Курс уже выбран')) != -1) or \
            (text.find('Выбран тариф') != -1):
        await call.message.edit_text(
            f"{text}\nhttps://telegra.ph/Izmajlov-Aleksandr-Ajratovich-07-14",
            parse_mode="HTML")
    else:
        await call.message.edit_text(
            f"{text}\nhttps://telegra.ph/Izmajlov-Aleksandr-Ajratovich-07-14",
            parse_mode="HTML",
            reply_markup=all_keyboards["course_select_without_desc"]())


async def callback_standard(call: types.CallbackQuery):
    # TODO task is to add information about the selected tariff to the database and put it in the basket
    text = call.message.text
    if text.find('https') != -1:
        text1 = text[:text.find('https')]
        text2 = text[text.find('https'):]
        await call.message.edit_text(f"{text1}Выбран тариф ""Стандарт""\n"
                                     f"{text2}", parse_mode="HTML")
    else:
        await call.message.edit_text(f"{text}\nВыбран тариф ""Стандарт""\n", parse_mode="HTML",
                                     reply_markup=all_keyboards["course_desc"]())


async def callback_pro(call: types.CallbackQuery):
    # TODO task is to add information about the selected tariff to the database and put it in the basket
    text = call.message.text
    if text.find('https') != -1:
        text1 = text[:text.find('https')]
        text2 = text[text.find('https'):]
        await call.message.edit_text(f"{text1}Выбран тариф ""ПРО""\n"
                                     f"{text2}", parse_mode="HTML")
    else:
        await call.message.edit_text(f"{text}\nВыбран тариф ""ПРО""", parse_mode="HTML",
                                     reply_markup=all_keyboards["student_detail"]())
