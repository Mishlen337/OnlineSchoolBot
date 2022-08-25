import aiosql
import asyncpg

from db.config import config
from db.utils import exceptions


async def turn_in_personal_lesson_homework(tg_id, lesson_id, file_id):
    conn = None
    query = aiosql.from_path(
        "./telegram/db/student/sql_files/homework.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.turn_in_personal_lesson_homework(
            conn, tg_id=tg_id, lesson_id=lesson_id, file_id=file_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()
