import aiosql
import asyncpg
from db.config import config


async def get_basket_content(user_id):
    # handle operation error
    query = aiosql.from_path("./db/student/sql_files/order.sql", driver_adapter="asyncpg")
    conn = await asyncpg.connect(config.DB_URI)
    result = await query.get_basket_content(conn, user_id)
    await conn.close()
    return result


async def _create_basket(user_id):
    # handle unique(student, status = неоплачено)
    # handle operation error
    pass

async def delete_basket(tg_id):
    # handle operation error
    pass
