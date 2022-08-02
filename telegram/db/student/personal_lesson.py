import aiosql
import asyncpg

from db.config import config
from db.utils import exceptions


async def get_available_teachers():
    "Authorizes student when he comes in bot."
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files/personal_lesson.sql",
                             driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_available_teachers(conn)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def get_personal_teacher_description(employee_id, subject_name):
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files/personal_lesson.sql",
                             driver_adapter="asyncpg")
    try:
        conn = await asyncpg.connect(config.DB_URI)
        description = (await query.get_personal_teacher_description(
            conn, employee_id=employee_id, subject_name=subject_name))['description']
        await conn.close()
        return description
    except KeyError:
        raise exceptions.NoSuchTutor()
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()
