from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from db.student.course import get_course_packages


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
