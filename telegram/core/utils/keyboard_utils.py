from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from db.student.course import get_course_packages
from db.student.personal_lesson import get_selected_personal_teachers


def add_course_desc_to_kb(kb: InlineKeyboardMarkup, course_id: int) -> None:
    kb.add(InlineKeyboardButton(text="Подробнее", callback_data="course_desc:" + str(course_id)))


async def add_course_packages_to_kb(kb_student: InlineKeyboardMarkup, course_id: int) -> None:
    packages_list = await get_course_packages(course_id)
    kb_student.row_width = (len(packages_list) if len(packages_list) > 0 else 1)
    for package in packages_list:
        kb_student.add(
            InlineKeyboardButton(
                text=package["package_name"],
                callback_data="add_course:" + str(course_id) + ":" + package["package_name"]),
        )


def add_personal_desc_to_kb(kb: InlineKeyboardMarkup, teacher_id: int, subject_name: str) -> None:
    kb.add(InlineKeyboardButton(
        text="Подробнее",
        callback_data="personal_desc:" + str(teacher_id) + ':' + subject_name))


def add_contact_to_kb(kb: InlineKeyboardMarkup, teacher_id: int, subject_name: str) -> None:
    kb.add(InlineKeyboardButton(
        text="Связяться",
        callback_data="add_personal:" + str(teacher_id) + ':' + subject_name))


def add_materials(kb: InlineKeyboardMarkup, tg_id: int) -> None:
    kb.row_width = 1
    kb.add(
        InlineKeyboardButton(text="Курсы", callback_data="add_course_materials:" + str(tg_id)),
        InlineKeyboardButton(text="Индивидуальные занятия", callback_data="add_personal_materials:" + str(tg_id))
    )


def add_course_materials(kb: InlineKeyboardMarkup, tg_id, course_id: int) -> None:
    kb.add(InlineKeyboardButton(
        text="Показать материалы",
        callback_data="show_course_materials:" + str(tg_id) + ":" + str(course_id))
    )


async def add_subjects(kb: InlineKeyboardMarkup, tg_id: int) -> None:
    subject_list = await get_selected_personal_teachers(tg_id)
    for sub in subject_list:
        kb.add(
            InlineKeyboardButton(
                text=sub["teacher_surname"] + ' ' + sub["teacher_name"] + ' ' + sub["subject_name"],
                callback_data="add_subject_and_teacher:" + str(tg_id) + ":" + str(sub["teacher_id"]) + ':' + sub[
                    "subject_name"]
            ))
