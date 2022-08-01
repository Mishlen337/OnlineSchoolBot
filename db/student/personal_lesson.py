import aiosql
import asyncpg

from db.config import config
from db.utils import exceptions


async def get_available_teachers():
    "Authorizes student when he comes in bot."
    conn = None
    query = aiosql.from_path("./db/student/sql_files/personal_lesson.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_available_teachers(conn)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()
