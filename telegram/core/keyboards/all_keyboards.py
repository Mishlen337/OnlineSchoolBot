from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
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


all_keyboards["student_menu"] = kb_student_menu
