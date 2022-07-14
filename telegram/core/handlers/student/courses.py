"""Module to declare handlers related with courses."""
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext
from core.keyboards.all_keyboards import all_keyboards

mathematics = {'id_course': 0,
        'name_course':'Математика подготовка к ЕГЭ',
        'name_subject':'Математика',
        'name_teacher':'Галаган Гомункулич Васильевич',
        'price_course':'1000 рублей',
        'Basket': True,
        'Selected': False}
physics = {'id_course': 1,
        'name_course':'Физика подготовка к ЕГЭ',
        'name_subject':'Физика',
        'name_teacher':'Калинина биг босс абудаби',
        'price_course':'12415 рублей',
        'Basket': False,
        'Selected': True}
informatics = {'id_course': 2,
        'name_course':'Информатика подготовка к ЕГЭ',
        'name_subject':'Информатика',
        'name_teacher':'Измайлов Марат Айратович',
        'price_course':'10000000 рублей',
        'Basket': False,
        'Selected': False}
Subjects = [mathematics,physics,informatics]

async def get_courses(message: types.Message, state: FSMContext):
    """Answers available courses."""
    logger.debug(f"Student {message.from_user} requests available courses.")
    # TODO send available courses to student
    num_of_courses = len(Subjects)
    if num_of_courses > 0:
        await message.answer("Сообщение о скидке.")
        for i in range(num_of_courses):
            Sub = Subjects[i]
            Info_course = (f"{Sub['name_course']}\n"
                                     f"{Sub['name_subject']}\n"
                                     f"{Sub['name_teacher']}\n"
                                     f"{Sub['price_course']}\n")
            if Sub['Basket']:
                await message.answer(f"{Info_course}Курс находится в корзине",parse_mode="HTML",
                                     reply_markup=all_keyboards["student_detail"]())
            elif Sub['Selected']:
                await message.answer(f"{Info_course}Курс уже выбран",parse_mode="HTML",
                                     reply_markup=all_keyboards["student_detail"]())
            else:
                await message.answer(f"{Info_course}",parse_mode="HTML",
                                     reply_markup=all_keyboards["student_tarifselect_1"]())
    else:
        await message.answer("Курсы отсутствуют.")

async def callback_detail(call: types.CallbackQuery):
    # TODO task is to send teacher questionnaires (or links to them)
    text = call.message.text
    if (text.find('Курс находится в корзине') != -1) or ((text.find('Курс уже выбран')) != -1):
        await call.message.edit_text(f"{text}\nhttps://telegra.ph/Izmajlov-Aleksandr-Ajratovich-07-14",
                                     parse_mode="HTML")
    else:
        await call.message.edit_text(f"{text}\nhttps://telegra.ph/Izmajlov-Aleksandr-Ajratovich-07-14",
                                     parse_mode="HTML",reply_markup=all_keyboards["student_tarifselect_2"]())

async def callback_standard(call: types.CallbackQuery):
    # TODO task is to add information about the selected tariff to the database and put it in the basket
    text = call.message.text
    if text.find('https') != -1:
        text1 = text[:text.find('https')]
        text2 = text[text.find('https'):]
        await call.message.edit_text(f"{text1}Выбран тариф ""Стандарт""\n"
                                     f"{text2}" ,parse_mode="HTML")
    else:
        await call.message.edit_text(f"{text}\nВыбран тариф ""Стандарт""\n", parse_mode="HTML")

async def callback_pro(call: types.CallbackQuery):
    # TODO task is to add information about the selected tariff to the database and put it in the basket
    text = call.message.text
    if text.find('https') != -1:
        text1 = text[:text.find('https')]
        text2 = text[text.find('https'):]
        await call.message.edit_text(f"{text1}Выбран тариф ""ПРО""\n"
                                     f"{text2}", parse_mode="HTML")
    else:
        await call.message.edit_text(f"{text}\nВыбран тариф ""ПРО""", parse_mode="HTML")