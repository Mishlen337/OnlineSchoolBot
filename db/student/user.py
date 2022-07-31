import aiosql
import asyncpg
from db.config import config


async def tg_auth(user_id):
    "Authorizes student when he comes in bot."
    # handle operation errors
    query = aiosql.from_path("./db/student/sql_files/user.sql", driver_adapter="asyncpg")
    conn = await asyncpg.connect(config.DB_URI)
    await query.tg_auth(conn, user_id)
    await conn.close()


async def info_init(user_id, name, patronymic, surname, email, class_num):
    "Initializes information about student"
    query = aiosql.from_path("./db/student/sql_files/user.sql", driver_adapter="asyncpg")
    conn = await asyncpg.connect(config.DB_URI)
    await query.info_init(conn, tg_id=user_id, name=name, patronymic=patronymic, surname=surname,
                          email=email,
                          class_num=class_num)
    await conn.close()
