from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from counters_api.repository.redis_repository import RedisRepository
    from counters_api.repository.db_repository import DBRepository

class SyncWorkerService:
    def __init__(
        self, 
        redis_repository: "RedisRepository", 
        db_repository: "DBRepository"
    ):
        self.db_repository = db_repository
        self.redis_repository = redis_repository

    async def sync_batch_redis_to_db(self, batch_size: int):
        video_ids = await self.redis_repository.get_updated_videos_ids(
            batch_size
        )
        
        video_mapping = await self.redis_repository.get_bulk_video_views(
            video_ids
        )
        await self.db_repository.bulk_update_videos(
            video_mapping
        )

    async def sync_batch_db_to_redis(self, limit: int, offset: int):
        videos = await self.db_repository.get_videos_paged(
            limit=limit,
            offset=offset
        )
        videos_mapping = [(v['id'], v['views']) for v in videos]

        await self.redis_repository.set_bulk_videos_views(videos_mapping)

    async def run_db_redis_sync(self, batch_size: int):
        total_videos = await self.db_repository.get_video_count()
        offset = 0
        for _ in range(total_videos // batch_size + 1):
            await self.sync_batch_db_to_redis(
                limit=batch_size,
                offset=offset
            )
            offset += offset

    async def run_redis_db_sync(self, batch_size: int, max_retry: int):
        updated_videos = await self.redis_repository.get_updated_videos_count()
        need_runs = updated_videos // batch_size 
        if updated_videos % batch_size != 0:
            need_runs += 1
            
        runs = min(need_runs, max_retry)
        for _ in range(runs):
            await self.sync_batch_redis_to_db(batch_size=batch_size)

   