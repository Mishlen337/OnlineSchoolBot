"""Module to declare handlers related with personal schedule."""
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext

mathematics = { 'id_course': 0,
        'name_course':'Математика подготовка к ЕГЭ',
        'name_subject':'Математика',
        'name_teacher':'Галаган Гомункулич Васильевич',
        'price_course':'100 рублей',
        'date': '21.08.2022 в 21:00',
        'link': 'https://youtu.be/HwhrPZuNJTY',
        'Basket': False,
        'Selected': True}
physics = {'id_course': 1,
        'name_course':'Физика подготовка к ЕГЭ',
        'name_subject':'Физика',
        'name_teacher':'Калинина биг босс абудаби',
        'price_course':'100 рублей',
        'date': '21.08.2022 в 21:00',
        'link': 'https://youtu.be/HwhrPZuNJTY',
        'Basket': False,
        'Selected': True}
informatics = {'id_course': 2,
        'name_course':'Информатика подготовка к ЕГЭ',
        'name_subject':'Информатика',
        'name_teacher':'Измайлов Марат Айратович',
        'price_course':'100 рублей',
        'date': '21.08.2022 в 21:00',
        'link': 'https://youtu.be/HwhrPZuNJTY',
        'Basket': False,
        'Selected': True}
Subjects = [mathematics,physics,informatics]
async def get_schedule(message: types.Message, state: FSMContext):
    "Answers student's personal schedule."
    logger.debug(f"Student {message.from_user} requests personal schedule.")
    # TODO send personal schedule
    num_subjects = len(Subjects)
    if num_subjects > 0:
        for i in range(num_subjects):
            sub = Subjects[i]
            Info_course = (f"{sub['name_course']}\n"
                           f"{sub['name_subject']}\n"
                           f"{sub['name_teacher']}\n"
                           f"{sub['date']}\n"
                           f"{sub['link']}")
            await message.answer(text=f"{Info_course}", parse_mode='HTML')
    else:
        await message.answer("В расписании ничего нет.")
