import aiosql
import asyncpg

from db.config import config
from db.utils import exceptions


async def get_personal_lessons_homeworks(tg_id):
    conn = None
    query = aiosql.from_path("./telegram/db/employee/sql_files/homeworks.sql",
                             driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_personal_lessons_homeworks(conn, tg_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def get_webinars_homeworks(tg_id):
    conn = None
    query = aiosql.from_path("./telegram/db/employee/sql_files/homeworks.sql",
                             driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_webinars_homeworks(conn, tg_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def get_group_lessons_homeworks(tg_id):
    conn = None
    query = aiosql.from_path("./telegram/db/employee/sql_files/homeworks.sql",
                             driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_group_lessons_homeworks(conn, tg_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def check_personal_homework(tg_id, lesson_id, file_id):
    conn = None
    query = aiosql.from_path("./telegram/db/employee/sql_files/homeworks.sql",
                             driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_personal_homework(conn, tg_id=tg_id, lesson_id=lesson_id, file_id=file_id)
        if not result:
            raise exceptions.AccessError()
        if result["checked_homework_file_id"]:
            raise exceptions.CheckError()
        await query.check_personal_homework(conn, tg_id=tg_id, lesson_id=lesson_id, file_id=file_id)
        await conn.close()
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def check_webinar_homework(tg_id, lesson_id, file_id):
    conn = None
    query = aiosql.from_path("./telegram/db/employee/sql_files/homeworks.sql",
                             driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_webinar_homework(conn, tg_id=tg_id, lesson_id=lesson_id, file_id=file_id)
        if not result:
            raise exceptions.AccessError()
        if result["checked_homework_file_id"]:
            raise exceptions.CheckError()
        await query.check_webinar_homework(conn, tg_id=tg_id, lesson_id=lesson_id, file_id=file_id)
        await conn.close()
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def check_group_lesson_homework(tg_id, lesson_id, file_id):
    conn = None
    query = aiosql.from_path("./telegram/db/employee/sql_files/homeworks.sql",
                             driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_group_lesson_homework(conn, tg_id=tg_id, lesson_id=lesson_id, file_id=file_id)
        if not result:
            raise exceptions.AccessError()
        if result["checked_homework_file_id"]:
            raise exceptions.CheckError()
        await query.check_group_lesson_homework(conn, tg_id=tg_id, lesson_id=lesson_id, file_id=file_id)
        await conn.close()
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()

