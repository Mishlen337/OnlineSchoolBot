from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.utils import deep_linking

from core.config import config
from core.keyboards import student_keyboards
from db.student import user
from db.utils import exceptions
from core.utils import messages


async def commands_handler(message: types.Message, state: FSMContext):
    match message.get_command()[1:]:
        case "start":
            args = message.get_args()
            if args == "employee":
                await message.answer("Привет, сотрудник")
                await message.answer("Для регистрации в боте, необходимо узнать ваш номер телефона.")
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                button_phone = types.KeyboardButton(text="Отправить номер телефона",
                                                    request_contact=True)
                keyboard.add(button_phone)
                await message.answer(
                    "Отправьте номер телефона (кнопка отправки встроена в клавиатуру)",
                    reply_markup=keyboard)
                await state.set_state("employee_telephone")
            else:
                await message.answer("Присоединяйся к нашей дружной семье!",
                                     reply_markup=student_keyboards.all_keyboards["menu"]())

                try:
                    await user.tg_auth(message.from_user.id)
                except exceptions.StudentExists:
                    pass
                except exceptions.ConnectionError:
                    await message.answer("Упс. Что то пошло не так")
                    return

                await state.set_state("student_main")
        case "stop":
            await message.answer(
                "Вы отключились от бота. Зайдите заново с помощью команды /start",
                reply_markup=ReplyKeyboardRemove(),
            )
            await state.reset_data()
            await state.reset_state()
        case "help":
            await message.answer(messages.HELP_MESSAGE)
        case "getlink":
            link = await deep_linking.get_start_link(payload='employee')
            await message.answer('Ссылка для входа с правами сотрудника\n{}'.format(link))
        case "terms":
            try:
                await message.answer("Условия оферты.")
                await message.bot.send_document(message.from_user.id, open(config.TERMS_PATH, 'rb'))
            except FileNotFoundError:
                await message.answer("Упс. Что то пошло не так")


async def base_handler(message: types.Message, state: FSMContext):
    await message.answer(messages.ERROR_MESSAGE)
