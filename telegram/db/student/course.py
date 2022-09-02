import aiosql
import asyncpg

from db.config import config
from db.utils import exceptions


async def get_courses(tg_id):
    # operation error
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files/course.sql", driver_adapter="asyncpg")

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
    query = aiosql.from_path("./telegram/db/student/sql_files/course.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_course_packages(conn, course_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def get_full_and_partly_purchased_courses(tg_id):
    conn = None
    query = aiosql.from_path(
        "./telegram/db/student/sql_files/course.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_full_and_partly_purchased_courses(conn, tg_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def get_pro_purchased_courses(tg_id):
    conn = None
    query = aiosql.from_path(
        "./telegram/db/student/sql_files/course.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_pro_purchased_courses(conn, tg_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def get_course_groups(course_id):
    conn = None
    query = aiosql.from_path(
        "./telegram/db/student/sql_files/course.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_course_groups(conn, course_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def group_sign_up(tg_id, group_id):
    conn = None
    query = aiosql.from_path(
        "./telegram/db/student/sql_files/course.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.group_sign_up(conn, tg_id=tg_id, group_id=group_id)
        await conn.close()
        return result

    except asyncpg.exceptions.TriggeredActionError:
        await conn.close()
        raise exceptions.AccessError()
    except asyncpg.exceptions.UniqueViolationError:
        await conn.close()
        raise exceptions.GroupSingUpError()
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()
