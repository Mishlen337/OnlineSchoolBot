import aiosql
import asyncpg

from db.config import config
from db.utils import exceptions


async def get_user_tg_id(employee_id):
    conn = None
    query = aiosql.from_path("./telegram/db/employee/sql_files/user.sql",
                             driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_user_tg_id(conn, employee_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()
