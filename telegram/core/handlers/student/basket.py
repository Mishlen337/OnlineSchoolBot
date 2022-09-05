"""Module to declare handlers related with basket."""
from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import MessageCantBeDeleted

from db.student import order
from db.student import course
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
        await message.answer("Упс. Что-то пошло не так")
        return

    if courses_list:
        try:
            message_id = await order.get_order_course_package_message_ids(tg_id=message.from_user.id)
            for id in message_id:
                if id["message_id"] is not None:
                    try:
                        await bot.delete_message(chat_id=message.chat.id, message_id=id["message_id"])
                        break
                    except MessageCantBeDeleted:
                        break
        except ConnectionError:
            await message.answer("Упс. Что-то пошло не так")
        await message.answer("Курсы в корзине: ",
                             parse_mode='HTML', reply_markup=all_keyboards["menubasket"]())
        course_prices = []
        msg_text = ''
        for crs in courses_list:
            course_prices.append(
                types.LabeledPrice(
                    label=f"{crs['course_name']} - {crs['package_name']}", amount=crs['price'] * 100))
            msg_text += BASKET_INFO_COURSE.format(
                course_name=crs['course_name'],
                subject_name=crs['subject_name'],
                teacher_name=crs['teacher_name'],
                teacher_patronymic=crs['teacher_patronymic'] if crs['teacher_patronymic'] != None else '',
                teacher_surname=crs['teacher_surname'],
                package=crs['package_name'],
                price=crs['price']
            ) + '\n'
        msg_text += '<b>Скидка: 10%</b>'
        await message.answer(text=msg_text, parse_mode='HTML')

        # course_prices.append(types.LabeledPrice(label='Скидка', amount=-100))
        send_message = await bot.send_invoice(message.chat.id,
                                              title='Выбранные курсы',
                                              description=' ',
                                              provider_token=config.PAYMENTS_SECRET,
                                              currency='rub',
                                              prices=course_prices,
                                              payload='pay-course-basket:'+str(message.message_id + 3),
                                              start_parameter='basket')
        await order.update_order_course_package_message_ids(tg_id=message.from_user.id,
                                                            message_id=send_message.message_id)
    else:
        await message.answer("Корзина пуста.")


async def checkout_process(pre_checkout_query: types.PreCheckoutQuery):
    try:
        message_id = await order.get_order_course_package_message_ids(tg_id=pre_checkout_query.from_user.id)
        ok = True
        check = int(pre_checkout_query.invoice_payload.split(':')[1])
        for id in message_id:
            if id["message_id"] != check:
                ok = False
                break
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=ok,
                                            error_message="Упс. Что-то пошло не так. Очистите корзину и попробуйте заново")
    except ConnectionError:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False, error_message="Упс. Что-то пошло не так")


async def successful_payment(message: types.Message):
    text = message.successful_payment
    try:
        basket_content = await order.get_basket_content(message.from_user.id)
        await order.purchase_basket(message.from_user.id)
        await message.answer(f"Оплата на сумму {text.total_amount // 100} {text.currency} прошла успешно",
                             parse_mode='HTML', reply_markup=all_keyboards["menu"]())

        for order_course_package in basket_content:
            if order_course_package["package_name"] == 'про':
                await message.answer(
                    f"Вам необходимо выбрать группу обучения на курсе <b>{order_course_package['course_name']}</b>.",
                    parse_mode="HTML",
                    reply_markup=await all_keyboards["choose_course_groups"](
                        message.from_user.id, order_course_package["course_id"]))
    except exceptions.ConnectionError:
        await message.answer("Упс. Что-то пошло не так")


async def clear_basket(message: types.Message):
    try:
        message_id = await order.get_order_course_package_message_ids(tg_id=message.chat.id)
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message_id[0]["message_id"])
        except MessageCantBeDeleted:
            pass
        await order.delete_basket(message.from_user.id)
        await message.answer("Корзина очищена", reply_markup=all_keyboards["menu"]())
    except exceptions.ConnectionError:
        await message.answer("Упс. Что-то пошло не так")

async def choose_group(callback: types.CallbackQuery):
    logger.debug(f"Student {callback.from_user} chose group.")
    tg_id, group_id = map(int, callback.data.split(':')[1:])
    try:
        await course.group_sign_up(tg_id, group_id)
    except exceptions.AccessError:
        await callback.answer("У вас нет прав записаться в группу.")
    except exceptions.GroupSingUpError:
        await callback.answer("Вы уже записались в группу.")
    except exceptions.ConnectionError:
        await callback.message.answer("Упс. Что-то пошло не так")
    await callback.message.edit_text(
        callback.message.text + "Вы успешно записались в группу.")
