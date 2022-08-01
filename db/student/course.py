import aiosql
import asyncpg

from db.config import config
from db.utils import exceptions


async def get_courses(tg_id):
    # operation error
    conn = None
    query = aiosql.from_path("./db/student/sql_files/course.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_courses(conn, tg_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def get_course_packages(course_id):
    conn = None
    query = aiosql.from_path("./db/student/sql_files/course.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_course_packages(conn, course_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()
