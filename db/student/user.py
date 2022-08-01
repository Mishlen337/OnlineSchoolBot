import aiosql
import asyncpg
from db.config import config
from db.utils import exceptions


async def tg_auth(tg_id):
    "Authorizes student when he comes in bot."
    conn = None
    query = aiosql.from_path("./db/student/sql_files/user.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        await query.tg_auth(conn, tg_id)
        await conn.close()
    except asyncpg.exceptions.UniqueViolationError:
        await conn.close()
        raise exceptions.StudentExists()
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def info_init(tg_id, name, patronymic, surname, email, class_num):
    "Initializes information about student"
    conn = None
    query = aiosql.from_path("./db/student/sql_files/user.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        await query.info_init(conn, tg_id=tg_id, name=name, patronymic=patronymic, surname=surname,
                              email=email,
                              class_num=class_num)
        await conn.close()
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()
