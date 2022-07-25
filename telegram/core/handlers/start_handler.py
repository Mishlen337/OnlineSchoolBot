from aiogram import types
from loguru import logger
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from core.keyboards.all_keyboards import all_keyboards
from aiogram.utils import deep_linking


async def commands_handler(message: types.Message, state: FSMContext):
    match message.get_command()[1:]:
        case "start":
            args = message.get_args()
            if args == "employee":
                await message.answer(f"Привет, сотрудник")
                await state.set_state("employee_main")
            else:
                await message.answer("Здесь будет приветственное слово и \
                    регистрация", reply_markup=all_keyboards["student_menu"]())
                # TODO registration
                await state.set_state("student_main")
        case "stop":
            await message.answer(
                "Вы отключились от бота. \
                    Зайдите заново с помощью команды /start",
                reply_markup=ReplyKeyboardRemove(),
            )
            await state.reset_data()
            await state.reset_state()
        case "help":
            await message.answer(
                "Страничка помощи (Здесь будет полезная инфа):\n\
            /start начать работу бота и приступить к авторизации через почту\n\
            /stop сбросить состояние бота \n\
            /help показать помощь"
            )
        case "getlink":
            link = await deep_linking.get_start_link(payload='employee')
            await message.answer('Ссылка для входа с правами сотрудника\n{}'.format(link))


async def base_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "К сожалению, ни один из обработчиков в данный момент не смог \
         обработать ваше сообщение в текущем состоянии. \
         Для того, чтобы сбросить состояние используйте команду /stop, \
         а затем /start"
    )
