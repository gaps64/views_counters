
import asyncpg
from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis.asyncio import Redis

from counters_api.api.api import router
from counters_api.container import Container
from counters_api.settings import settings

async def lifespan(app: FastAPI):
    
    pg_pool = await asyncpg.create_pool(
        # dsn postgres://user:pass@host:port/database?option=value.
        dsn=f'postgres://{settings.db_user}:{settings.db_password}@'
            f'{settings.db_host}:{settings.db_port}/{settings.db_name}',
        min_size=settings.dd_pool_min_size,
        max_size=20,
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
    # app.state.container = container
    app.container = container

    yield
 
    await redis.close()
    await pg_pool.close()
  

app = FastAPI(title="View Counter",
              lifespan=lifespan)

app.include_router(router)






