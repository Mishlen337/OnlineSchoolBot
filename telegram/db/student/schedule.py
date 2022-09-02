import aiosql
import asyncpg

from db.config import config
from db.utils import exceptions


async def get_personal_lessons_schedule(tg_id):
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files/schedule.sql",
                             driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_personal_lessons_schedule(conn, tg_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def get_purchased_webinars_schedule(tg_id):
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files/schedule.sql",
                             driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_purchased_webinars_schedule(conn, tg_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def get_group_lessons_schedule(tg_id):
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files/schedule.sql",
                             driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_group_lessons_schedule(conn, tg_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()
