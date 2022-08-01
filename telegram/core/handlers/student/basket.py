"""Module to declare handlers related with basket."""
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext
from core.utils.messages import BASKET_INFO_COURSE
from core.keyboards.student_keyboards import all_keyboards
from core.config import bot, config

mathematics = {'id': 0,
               'name': 'Математика подготовка к ЕГЭ',
               'course_subject_name': 'Математика',
               'teacher_subject_name': 'Галаган Гомункулич Васильевич',
               'price_course_standard': '100 рублей',
               'price_course_pro': '200 рублей',
               'begin_at': '21.08.2022 в 21:00',
               'end_at': '28.07.2023',
               'tariff': True,
               'Basket': True,
               'Selected': False}
physics = {'id': 1,
           'name': 'Физика подготовка к ЕГЭ',
           'course_subject_name': 'Физика',
           'teacher_subject_name': 'Калинина биг босс абудаби',
           'price_course_standard': '100 рублей',
           'price_course_pro': '200 рублей',
           'begin_at': '21.08.2022 в 21:00',
           'end_at': '28.07.2023',
           'tariff': False,
           'Basket': True,
           'Selected': False}
informatics = {'id': 2,
               'name': 'Информатика подготовка к ЕГЭ',
               'course_subject_name': 'Информатика',
               'teacher_subject_name': 'Измайлов Марат Айратович',
               'price_course_standard': '100 рублей',
               'price_course_pro': '200 рублей',
               'begin_at': '21.08.2022 в 21:00',
               'end_at': '28.07.2023',
               'tariff': True,
               'Basket': True,
               'Selected': False}
courses_list = [mathematics, physics, informatics]


async def get_basket(message: types.Message, state: FSMContext):
    """Answers basket's content."""
    logger.debug(f"Student {message.from_user} requests basket's content.")
    # TODO send basket's content
    num_of_courses = len(courses_list)
    if num_of_courses > 0:
        await message.answer("Курсы в корзине: ",
                             parse_mode='HTML', reply_markup=all_keyboards["menubasket"]())
        course_prices = []
        msg_text = ''
        for course in courses_list:
            if course['tariff']:
                price = int(course['price_course_pro'].split(" ")[0]) * 100
            else:
                price = int(course['price_course_standard'].split(" ")[0]) * 100
            course_prices.append(types.LabeledPrice(label=course['name'], amount=price))
            msg_text += BASKET_INFO_COURSE.format(
                name=course['name'],
                course_subject_name=course['course_subject_name'],
                teacher_subject_name=course['teacher_subject_name'],
                tariff='Стандарт' if not course['tariff'] else 'ПРО',
                selected_tariff=course['price_course_standard'] if not course['tariff'] else course['price_course_pro'],
                begin_at=course['begin_at'],
                end_at=course['end_at']
            )
        msg_text += '<b>Скидка: 10%</b>'
        await message.answer(text=msg_text, parse_mode='HTML')
        course_prices.append(types.LabeledPrice(label='Скидка', amount=-100 * 100))
        await bot.send_invoice(message.chat.id,
                               title='Выбранные курсы',
                               description=' ',
                               provider_token=config.PAYMENTS_SECRET,
                               currency='rub',
                               prices=course_prices,
                               payload='pay-course-basket',
                               start_parameter='basket')
    else:
        await message.answer("Корзина пуста.")


async def checkout_process(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def successful_payment(message: types.Message):
    text = message.successful_payment
    await message.answer(f"Оплата на сумму {text.total_amount // 100} {text.currency} прошла успешно",
                         parse_mode='HTML')
    # TODO delete the purchased course from the database


async def clear_basket(message: types.Message):
    # TODO еmpty the trash in the database
    await message.answer("Корзина очищена", reply_markup=all_keyboards["menu"]())
