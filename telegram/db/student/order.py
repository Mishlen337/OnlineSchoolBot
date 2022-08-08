from datetime import datetime
import aiosql
import asyncpg

from db.config import config
from db.utils import exceptions


async def get_basket_content(tg_id):
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files/order.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.get_basket_content(conn, tg_id)
        await conn.close()
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def purchase_basket(tg_id):
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files", driver_adapter="asyncpg")
    try:
        conn = await asyncpg.connect(config.DB_URI)
        student_id = (await query.get_id(conn, tg_id))["id"]
        await query.purchase_basket(conn, student_id)
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def add_course_package(tg_id, course_id, package_name):
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files", driver_adapter="asyncpg")
    try:
        conn = await asyncpg.connect(config.DB_URI)
        student_id = (await query.get_id(conn, tg_id))["id"]
        order_id = None

        try:
            order_id = (await query._create_basket(conn, student_id=student_id,
                                                   order_time=datetime.now()))["id"]
        except asyncpg.exceptions.UniqueViolationError:
            order_id = (await query._get_order_id(conn, student_id=student_id))["id"]

        try:
            await query.add_course_package(conn, order_id, student_id, course_id, package_name)
            await conn.close()
        except asyncpg.exceptions.ForeignKeyViolationError:
            await conn.close()
            raise exceptions.NoSuchCoursePackage()
        except asyncpg.exceptions.UniqueViolationError:
            course_order_status = await query._get_order_course_status(conn, order_id, student_id,
                                                                       course_id)
            await conn.close()
            raise exceptions.OrderCourseExists(course_order_status)
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def delete_basket(tg_id):
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        student_id = (await query.get_id(conn, tg_id))["id"]

        await query.delete_basket(conn, student_id)
        await conn.close()
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def get_order_course_package_message_ids(tg_id):
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files/order.sql", driver_adapter="asyncpg")
    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = (await query.get_order_course_package_message_ids(conn, tg_id))
        return result
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def update_order_course_package_message_ids(tg_id, message_id):
    conn = None
    query = aiosql.from_path("./telegram/db/student/sql_files", driver_adapter="asyncpg")
    try:
        conn = await asyncpg.connect(config.DB_URI)
        student_id = (await query.get_id(conn, tg_id))["id"]
        order_id = (await query._get_order_id(conn, student_id=student_id))["id"]
        await query.update_order_course_package_message_ids(conn, message_id=message_id,
                                                            order_id=order_id)
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()
