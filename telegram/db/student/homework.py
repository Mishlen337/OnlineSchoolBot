import aiosql
import asyncpg

from db.config import config
from db.utils import exceptions


async def turn_in_personal_lesson_homework(tg_id, lesson_id, file_id):
    conn = None
    query = aiosql.from_path(
        "./telegram/db/student/sql_files/homework.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)

        if await query.get_personal_lesson_access(conn, tg_id=tg_id, lesson_id=lesson_id):
            result = await query.turn_in_personal_lesson_homework(
                conn, lesson_id=lesson_id, file_id=file_id)
            await conn.close()
            return result
        else:
            await conn.close()
            raise exceptions.AccessError()
    except asyncpg.exceptions.UniqueViolationError:
        await conn.close()
        raise exceptions.DoneHomeworkExists()
    except asyncpg.exceptions.UnknownPostgresError:
        await conn.close()
        raise exceptions.NoSuchLessonOrNoAssistants()
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()


async def turn_in_webinar_homework(tg_id, webinar_id, file_id):
    conn = None
    query = aiosql.from_path(
        "./telegram/db/student/sql_files/homework.sql", driver_adapter="asyncpg")

    try:
        conn = await asyncpg.connect(config.DB_URI)
        result = await query.turn_in_webinar_homework(
            conn, tg_id=tg_id, webinar_id=webinar_id, file_id=file_id)
        await conn.close()
        return result

    except asyncpg.exceptions.UniqueViolationError:
        await conn.close()
        raise exceptions.DoneHomeworkExists()
    except asyncpg.exceptions.UnknownPostgresError:
        await conn.close()
        raise exceptions.NoSuchWebinarOrNoAssistants()
    except (asyncpg.PostgresConnectionError, OSError):
        if conn:
            await conn.close()
        raise exceptions.ConnectionError()
