import logging
from typing import AsyncContextManager

import aiopg
import logger
from aiopg import Connection
from psycopg2.extras import RealDictCursor

from app.core.config import Settings

logger = logging.getLogger(__name__)

async def initialize_postgres_pool():
    conf = Settings()
    global POOL

    POOL = await aiopg.create_pool(
        minsize=0,
        maxsize=5,
        timeout=60,
        pool_recycle=15,
        **{
            "host": conf.POSTGRES_HOST,
            "port": int(conf.POSTGRES_PORT),
            "database": conf.POSTGRES_DB_NAME,
            "user": conf.POSTGRES_USER,
            "password": conf.POSTGRES_PASSWORD.get_secret_value(),
            "cursor_factory": RealDictCursor
        })
    logger.info("Pool de connexions à PostgreSQL initialisé")


async def close_postgres_pool():
    if POOL:
        POOL.close()
        await POOL.wait_closed()
    logger.info("Pool de connexions à PostgreSQL fermé")

def connection_async() -> AsyncContextManager[Connection]:
    return POOL.acquire()