"""Module to declare message templates."""
TUTOR_MESSAGE = '''Предмет: <b>{subject_name}</b>
Преподаватель: <b>{teacher_surname} {teacher_name} {teacher_patronymic}</b>
'''

SELECT_INFO_COURSE = '''Курс: <b>{course_name}</b>
Предмет: <b>{subject_name}</b>
Преподаватель: <b>{teacher_surname} {teacher_name} {teacher_patronymic}</b>
Дата начала курса: <b>{begin_at}</b>
Дата конца курса: <b>{end_at}</b>
'''

BASKET_INFO_COURSE = '''Курс: <b>{course_name}</b>
Предмет: <b>{subject_name}</b>
Преподаватель: <b>{teacher_surname} {teacher_name} {teacher_patronymic}</b>
Пакет: <b>{package}</b>
Цена: <b>{price}</b>
'''


SCHEDULE_INFO_PERSONAL = '''
Предмет: <b>{subject_name}</b>
Преподаватель: <b>{teacher_surname} {teacher_name} {teacher_patronymic}</b>
Начало: <b>{begin_at}</b>
Окончание: <b>{end_at}</b>
Ссылка на занятие: <b>{broadcast_link}</b>
'''

SCHEDULE_INFO_WEBINARS = '''
Курс: <b>{course_name}</b>
Тема: <b>{theme}</b>
Предмет: <b>{subject_name}</b>
Преподаватель: <b>{teacher_surname} {teacher_name} {teacher_patronymic}</b>
Начало: <b>{begin_at}</b>
Окончание: <b>{end_at}</b>
Ссылка на вебинар: <b>{broadcast_link}</b>
'''

SCHEDULE_INFO_GROUP_LESSONS = '''
Курс: <b>{course_name}</b>
Группа: <b>{group_type}</b>
Тема: <b>{theme}</b>
Предмет: <b>{subject_name}</b>
Преподаватель: <b>{teacher_surname} {teacher_name} {teacher_patronymic}</b>
Начало: <b>{begin_at}</b>
Окончание: <b>{end_at}</b>
Ссылка на вебинар: <b>{broadcast_link}</b>
'''

INFO_WEBINAR_COURSE_MATERIALS = '''
Курс: <b>{course_name}</b>
Преподаватель: <b>{teacher_surname} {teacher_name} {teacher_patronymic}</b>
Ссылка на группу: <b>{tg_group_link}</b>
'''

INFO_WEBINARS_ONLINE = '''
Тема: <b>{theme}</b>
Формат: <b>{format}</b>
Начало: <b>{begin_at}</b>
Конец: <b>{end_at}</b>
Ссылка: <b>{record_link}</b>
Конспект: <b>{material_link}</b>
Домашнее задание: <b>{homework_link}</b>
Дедлайн дз: <b>{homework_deadline_time}</b>
'''

INFO_WEBINARS_RECORD = '''
Тема: <b>{theme}</b>
Формат: <b>{format}</b>
Ссылка: <b>{record_link}</b>
Конспект: <b>{material_link}</b>
Домашнее задание: <b>{homework_link}</b>
Дедлайн дз: <b>{homework_deadline_time}</b>
'''

INFO_PERSONAL_LESSONS = '''
Начало: <b>{begin_at}</b>
Конец: <b>{end_at}</b>
Ссылка: <b>{record_link}</b>
Конспект: <b>{material_link}</b>
Домашнее задание: <b>{homework_link}</b>
Дедлайн дз: <b>{homework_deadline_time}</b>
'''

INFO_PERSONAL_TEACHERS = '''
Преподаватель: <b>{teacher_surname} {teacher_name} {teacher_patronymic}</b>
Предмет: <b>{subject_name}</b>
'''

INFO_GROUP_COURSE_MATERIALS = '''
Курс: <b>{course_name}</b>
Преподаватель: <b>{teacher_surname} {teacher_name} {teacher_patronymic}</b>
Ссылка на группу: <b>{tg_group_link}</b>
'''

INFO_GROUP_LESSONS = '''
Тема: <b>{theme}</b>
Начало: <b>{begin_at}</b>
Конец: <b>{end_at}</b>
Ссылка: <b>{record_link}</b>
Конспект: <b>{material_link}</b>
Домашнее задание: <b>{homework_link}</b>
Дедлайн дз: <b>{homework_deadline_time}</b>
'''

HELP_MESSAGE = '''
Страничка помощи (Здесь будет полезная инфа):
/stop - сбросить состояние бота
/terms - прочитать условия оферты
Если что-то пошло не так, пишите @mishlen25
'''

ERROR_MESSAGE = '''
К сожалению, ни один из обработчиков в данный момент не смог \
обработать ваше сообщение в текущем состоянии. \
Для того, чтобы сбросить состояние используйте команду /stop, \
а затем /start
'''
