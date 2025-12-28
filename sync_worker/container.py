from dependency_injector import containers, providers

from counters_api.repository.redis_repository import RedisRepository
from counters_api.repository.db_repository import DBRepository
from sync_worker.sync_worker_service import SyncWorkerService


class Container(containers.DeclarativeContainer):

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
    sync_worker = providers.Factory(
        SyncWorkerService,
        redis_repository=redis_repository,
        db_repository=db_repository,
    )