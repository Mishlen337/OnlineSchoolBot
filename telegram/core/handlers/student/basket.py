"""Module to declare handlers related with basket."""
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext

from core.keyboards.student_keyboards import all_keyboards
from core.config import bot, config

mathematics = {'id_course': 0,
               'name_course': 'Математика подготовка к ЕГЭ',
               'name_subject': 'Математика',
               'name_teacher': 'Галаган Гомункулич Васильевич',
               'price_course': '100 рублей',
               'Basket': True,
               'Selected': False}
physics = {'id_course': 1,
           'name_course': 'Физика подготовка к ЕГЭ',
           'name_subject': 'Физика',
           'name_teacher': 'Калинина биг босс абудаби',
           'price_course': '100 рублей',
           'Basket': True,
           'Selected': False}
informatics = {'id_course': 2,
               'name_course': 'Информатика подготовка к ЕГЭ',
               'name_subject': 'Информатика',
               'name_teacher': 'Измайлов Марат Айратович',
               'price_course': '100 рублей',
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
        info_course = ''
        for course in courses_list:
            price = int(course['price_course'].split(" ")[0])*100
            course_prices.append(types.LabeledPrice(label=course['name_course'], amount=price))
            info_course += (f"{course['name_subject']}\n{course['name_teacher']}\n\n")
        await bot.send_invoice(message.chat.id,
                               title='Выбранные курсы',
                               description=info_course,
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
    await message.answer(f"Оплата на сумму {text.total_amount//100} {text.currency} прошла успешно",
                         parse_mode='HTML')
    # TODO delete the purchased course from the database


async def clear_basket(message: types.Message):
    # TODO еmpty the trash in the database
    await message.answer("Корзина очищена", reply_markup=all_keyboards["menu"]())
