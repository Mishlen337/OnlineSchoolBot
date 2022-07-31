import aiosql
import asyncpg
from db.config import config


async def get_personal_lessons_schedule(user_id):
    # handle operation error
    query = aiosql.from_path("./db/student/sql_files/schedule.sql", driver_adapter="asyncpg")
    conn = await asyncpg.connect(config.DB_URI)
    result = await query.get_personal_lessons_schedule(conn, user_id)
    await conn.close()
    return result


async def get_purchased_webinars_schedule(user_id):
    # handle operation error
    query = aiosql.from_path("./db/student/sql_files/schedule.sql", driver_adapter="asyncpg")
    conn = await asyncpg.connect(config.DB_URI)
    result = await query.get_purchased_webinars_schedule(conn, user_id)
    await conn.close()
    return result
