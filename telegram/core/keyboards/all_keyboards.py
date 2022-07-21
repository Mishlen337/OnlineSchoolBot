from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

all_keyboards = {}

def kb_student_menu():
    kb_student = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_student.add(
        KeyboardButton("Выбрать курсы"),
        KeyboardButton("Выбрать индивидуальные занятия"),
        KeyboardButton("Мое рассписание"),
        KeyboardButton("Корзина")
    )
    return kb_student

def ib_student_tarifselect_1():
    kb_student = InlineKeyboardMarkup(row_width=2)
    kb_student.add(
        InlineKeyboardButton(text="Добавить стандарт",callback_data="standard"),
        InlineKeyboardButton(text="Добавить ПРО",callback_data="pro"),
        InlineKeyboardButton(text="Подробнее", callback_data="detail")
    )
    return kb_student

def ib_student_tarifselect_2():
    kb_student = InlineKeyboardMarkup(row_width=2)
    kb_student.add(
        InlineKeyboardButton(text="Добавить стандарт",callback_data="standard"),
        InlineKeyboardButton(text="Добавить ПРО",callback_data="pro"),
    )
    return kb_student

def ib_student_detail():
    kb_student = InlineKeyboardMarkup()
    kb_student.add(InlineKeyboardButton(text="Подробнее", callback_data="detail"))
    return kb_student

def kb_student_menubasket():
    kb_student = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_student.add(
        KeyboardButton("Выбрать курсы"),
        KeyboardButton("Выбрать индивидуальные занятия"),
        KeyboardButton("Мое рассписание"),
        KeyboardButton("Очистить корзину")
    )
    return kb_student

all_keyboards["student_menu"] = kb_student_menu
all_keyboards["student_tarifselect_1"] = ib_student_tarifselect_1
all_keyboards["student_detail"] = ib_student_detail
all_keyboards["student_tarifselect_2"] = ib_student_tarifselect_2
all_keyboards["student_menubasket"] = kb_student_menubasket