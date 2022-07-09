from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from core.keyboards.all_keyboards import all_keyboards


async def commands_handler(message: types.Message, state: FSMContext):
    match message.text[1:]:
        case "start":
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


async def base_handler(message: types.Message, state: FSMContext):
    await message.answer(
        "К сожалению, ни один из обработчиков в данный момент не смог \
         обработать ваше сообщение в текущем состоянии. \
         Для того, чтобы сбросить состояние используйте команду /stop, \
         а затем /start"
    )
