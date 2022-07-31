import aiosql
import asyncpg
from db.config import config


async def get_available_teachers():
    "Authorizes student when he comes in bot."
    # handle operation errors
    query = aiosql.from_path("./db/student/sql_files/personal_lesson.sql", driver_adapter="asyncpg")
    conn = await asyncpg.connect(config.DB_URI)
    result = await query.get_available_teachers(conn)
    await conn.close()
    return result
