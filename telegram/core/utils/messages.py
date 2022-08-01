"""Module to declare message templates."""
PERSONAL_LESSON_MESSAGE = '''<b>Преподаватель: {teacher_name}</b>
Название занятия: {lesson_title}
Место проведения: {place}
'''

SELECT_INFO_COURSE = '''Курс: <b>{course_name}</b>
Предмет: <b>{subject_name}</b>
Преподаватель: <b>{teacher_name} {teacher_patronymic} {teacher_surname}</b>
Дата начала курса: <b>{begin_at}</b>
Дата конца курса: <b>{end_at}</b>
'''

BASKET_INFO_COURSE = '''Курс: <b>{course_name}</b>
Предмет: <b>{subject_name}</b>
Преподаватель: <b>{teacher_name} {teacher_patronymic} {teacher_surname}</b>
Пакет: <b>{package}</b>
Цена: <b>{price}</b>
'''


SCHEDULE_INFO_PERSONAL = '''<b>Предмет: {subject_name}</b>
Преподаватель: <b>{teacher_name} {teacher_patronymic} {teacher_surname}</b>
Название предмета: <b>{subject_name}</b>
Начало: <b>{begin_at}</b>
Окончание: <b>{end_at}</b>
Ссылка на занятие: <b>{broadcast_link}</b>
'''

SCHEDULE_INFO_WEBINARS = '''
Курс: <b>{course_name}</b>
Тема: <b>{theme}</b>
Предмет: <b>{subject_name}</b>
Преподаватель: <b>{teacher_name} {teacher_patronymic} {teacher_surname}</b>
Название предмета: <b>{subject_name}</b>
Начало: <b>{begin_at}</b>
Окончание: <b>{end_at}</b>
Ссылка на вебинар: <b>{broadcast_link}</b>
'''
