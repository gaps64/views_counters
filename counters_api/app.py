
import asyncpg
from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis.asyncio import Redis

from counters_api.api import api as api_module

from counters_api.api.api import router
from counters_api.container import Container
from counters_api.settings import settings

async def lifespan(app: FastAPI):
    
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
    container.wire(
        modules=[api_module]
    )
    # app.state.container = container
    app.container = container

    yield
 
    await redis.close()
    await pg_pool.close()
  

app = FastAPI(title="View Counter",
              lifespan=lifespan,
              version='1.0.0')

app.include_router(router)






