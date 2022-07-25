"""Module to declare handlers related with personal schedule."""
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext

mathematics = {'id_course': 0,
               'name_course': 'Математика подготовка к ЕГЭ',
               'name_subject': 'Математика',
               'name_teacher': 'Галаган Гомункулич Васильевич',
               'price_course': '100 рублей',
               'date': '21.08.2022 в 21:00',
               'link': 'https://youtu.be/HwhrPZuNJTY',
               'Basket': False,
               'Selected': True}
physics = {'id_course': 1,
           'name_course': 'Физика подготовка к ЕГЭ',
           'name_subject': 'Физика',
           'name_teacher': 'Калинина биг босс абудаби',
           'price_course': '100 рублей',
           'date': '21.08.2022 в 21:00',
           'link': 'https://youtu.be/HwhrPZuNJTY',
           'Basket': False,
           'Selected': True}
informatics = {'id_course': 2,
               'name_course': 'Информатика подготовка к ЕГЭ',
               'name_subject': 'Информатика',
               'name_teacher': 'Измайлов Марат Айратович',
               'price_course': '100 рублей',
               'date': '21.08.2022 в 21:00',
               'link': 'https://youtu.be/HwhrPZuNJTY',
               'Basket': False,
               'Selected': True}

lessons_list = [mathematics, physics, informatics]


async def get_schedule(message: types.Message, state: FSMContext):
    "Answers student's personal schedule."
    logger.debug(f"Student {message.from_user} requests personal schedule.")
    # TODO send personal schedule
    num_subjects = len(lessons_list)
    if num_subjects > 0:
        for lesson in lessons_list:
            lesson_info = f"{lesson['name_course']}\n{lesson['name_subject']}\n\
                {lesson['name_teacher']}\n{lesson['date']}\n{lesson['link']}"
            await message.answer(text=f"{lesson_info}", parse_mode='HTML')
    else:
        await message.answer("В расписании ничего нет.")
