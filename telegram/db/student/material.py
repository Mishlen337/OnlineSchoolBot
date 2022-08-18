import aiosql
import asyncpg

from db.config import config
from db.utils import exceptions


async def get_webinar_materials(tg_id, course_id):
    conn = None
    query = aiosql.from_path(
        "./telegram/db/student/sql_files/material.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_webinar_materials(conn, tg_id=tg_id, course_id=course_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def get_personal_lessons_materials(tg_id):
    conn = None
    query = aiosql.from_path(
        "./telegram/db/student/sql_files/material.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_personal_lessons_materials(conn, tg_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()
