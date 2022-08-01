"""Module to declare handlers related with basket."""
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext

from db.student import order
from db.utils import exceptions

from core.utils.messages import BASKET_INFO_COURSE
from core.keyboards.student_keyboards import all_keyboards
from core.config import bot, config


async def get_basket(message: types.Message, state: FSMContext):
    """Answers basket's content."""
    logger.debug(f"Student {message.from_user} requests basket's content.")
    courses_list = []
    
    try:
        courses_list = await order.get_basket_content(message.from_user.id)
    except ConnectionError:
        await message.answer("Упс. Что то пошло не так")
        return
    """select c.name as course_name, c.subject_name as course_subject_name,
       e.name as teacher_name, e.patronymic as teacher_patronymic, e.surname as teacher_surname,
       ocp.package_name, ocp.old_price as price"""
    
    if courses_list:
        await message.answer("Курсы в корзине: ",
                             parse_mode='HTML', reply_markup=all_keyboards["menubasket"]())
        course_prices = []
        msg_text = ''
        for crs in courses_list:
            course_prices.append(
                types.LabeledPrice(
                    label=f"{crs['course_name']} - {crs['package_name']}", amount=crs['price']*100))
            msg_text += BASKET_INFO_COURSE.format(
                course_name=crs['course_name'],
                subject_name=crs['subject_name'],
                teacher_name=crs['teacher_name'],
                teacher_patronymic=crs['teacher_patronymic'],
                teacher_surname=crs['teacher_surname'],
                package=crs['package_name'],
                price=crs['price']
            )
        msg_text += '<b>Скидка: 10%</b>'
        await message.answer(text=msg_text, parse_mode='HTML')

        # course_prices.append(types.LabeledPrice(label='Скидка', amount=-100))
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
    try:
        await order.purchase_basket(message.from_user.id)
        await message.answer(f"Оплата на сумму {text.total_amount // 100} {text.currency} прошла успешно",
                             parse_mode='HTML')
    except exceptions.ConnectionError:
        await message.answer("Упс. Что то пошло не так")


async def clear_basket(message: types.Message):
    try:
        await order.delete_basket(message.from_user.id)
        await message.answer("Корзина очищена", reply_markup=all_keyboards["menu"]())
    except exceptions.ConnectionError:
        await message.answer("Упс. Что то пошло не так")
