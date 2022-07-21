"""Module to declare handlers related with basket."""
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext
from core.keyboards.all_keyboards import all_keyboards
from core.config import bot, dp, config

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
        'price_course':'1000 рублей',
        'Basket': True,
        'Selected': False}
informatics = {'id_course': 2,
        'name_course':'Информатика подготовка к ЕГЭ',
        'name_subject':'Информатика',
        'name_teacher':'Измайлов Марат Айратович',
        'price_course':'1000 рублей',
        'Basket': True,
        'Selected': False}
Subjects = [mathematics,physics,informatics]

async def get_basket(message: types.Message, state: FSMContext):
    """Answers basket's content."""
    logger.debug(f"Student {message.from_user} requests basket's content.")
    # TODO send basket's content
    num_of_courses = len(Subjects)
    if num_of_courses > 0:
        await message.answer(f"Курсы в корзине: ",parse_mode='HTML', reply_markup=all_keyboards["student_menubasket"]())
        for i in range(num_of_courses):
            Sub = Subjects[i]
            price = int(Sub['price_course'].split(" ")[0])*100
            PRICES = [types.LabeledPrice(label=Sub['name_course'], amount=price)]
            Info_course = (f"{Sub['name_subject']}\n"
                           f"{Sub['name_teacher']}\n")
            await bot.send_invoice(message.chat.id,
                                   title=Sub['name_course'],
                                   description=Info_course,
                                   provider_token=config.PAYMENTS_SECRET,
                                   currency='rub',
                                   prices=PRICES,
                                   payload=Sub['name_subject'],
                                   start_parameter='basket')
    else:
        await message.answer("Корзина пуста.")

async def checkout_process(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

async def successful_payment(message: types.Message):
    text = message.successful_payment
    await message.answer(f"Оплата на сумму {text.total_amount//100} {text.currency} прошла успешно",parse_mode='HTML')
    # TODO delete the purchased course from the database

async def clear_basket(message: types.Message):
    # TODO еmpty the trash in the database
    await message.answer("Корзина очищена",reply_markup=all_keyboards["student_menu"]())