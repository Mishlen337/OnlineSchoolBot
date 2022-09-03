import aiosql
import asyncpg

from db.config import config
from db.utils import exceptions


async def auth_employee(tg_id, telephone):
    conn = None
    query = aiosql.from_path("./telegram/db/employee/sql_files/auth.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.auth_employee(conn, tg_id=tg_id, telephone=telephone)
        await conn.close()
        if not result:
            raise exceptions.AuthError()
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()
