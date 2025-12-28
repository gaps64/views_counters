import asyncio
from typing import TYPE_CHECKING

import asyncpg
from redis.asyncio import Redis

from counters_api.settings import settings
from sync_worker.container import Container


async def main():
    # Подключение к Redis
    pg_pool = await asyncpg.create_pool(
        # dsn postgres://user:pass@host:port/database?option=value.
        dsn=f'postgres://{settings.postgres_user}:{settings.postgres_password}@'
            f'{settings.postgres_host}:{settings.postgres_port}/'
            f'{settings.postgres_db}',
        min_size=settings.postgres_pool_min_size,
        max_size=settings.postgres_pool_max_size
    )

    redis = Redis.from_url(
        #app.state.redis_url = "redis://redis:6379"
        f'redis://{settings.redis_host}:{settings.redis_port}',
        decode_responses=True,
    )

    container = Container(
        pg_pool=pg_pool,
        redis=redis,
    )

    worker = container.sync_worker()

    try:
        while True:
            await worker.run_redis_db_sync(
                batch_size=settings.sync_batch_size,
                max_retry=settings.sync_max_retry
            )
            await asyncio.sleep(settings.sync_interval)
    finally:
        await redis.aclose()
        await pg_pool.close()


if __name__ == "__main__":
    asyncio.run(main())