from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from counters_api.repository.db_repository import DBRepository
from counters_api.repository.redis_repository import RedisRepository
from counters_api.service.views_service import ViewsService

class Container(DeclarativeContainer):

    redis = providers.Dependency()
    pg_pool = providers.Dependency()

    redis_repository = providers.Factory(
        RedisRepository,
        redis=redis,
    )
    db_repository = providers.Factory(
        DBRepository,
        pool=pg_pool,
    )
    views_service = providers.Factory(
        ViewsService,
        redis_repository=redis_repository,
        db_repository=db_repository,
    )