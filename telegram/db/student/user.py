import aiosql
import asyncpg
from db.config import config
from db.utils import exceptions


async def tg_auth(tg_id):
    "Authorizes student when he comes in bot."
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files/user.sql", driver_adapter="asyncpg")

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


async def telephone_init(tg_id, telephone: str):
    "Initializes telephone information about student"
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files/user.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        await query.telephone_init(conn, tg_id=tg_id, telephone=telephone)
        await conn.close()
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def fio_init(tg_id, name, patronymic, surname):
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files/user.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        await query.fio_init(conn, tg_id=tg_id,
                             name=name, patronymic=patronymic, surname=surname)
        await conn.close()
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def class_num_init(tg_id, class_num):
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files/user.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        await query.class_num_init(conn, tg_id=tg_id, class_num=class_num)
        await conn.close()
    except asyncpg.exceptions.CheckViolationError:
        await conn.close()
        raise exceptions.FormatError()
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def get_user_info(tg_id):
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files/user.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_user_info(conn, tg_id=tg_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def get_all_users():
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files/user.sql", driver_adapter="asyncpg")
    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_all_users(conn)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()
