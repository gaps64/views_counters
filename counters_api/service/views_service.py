from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from counters_api.repository.db_repository import DBRepository
    from counters_api.repository.redis_repository import RedisRepository

class ViewsService:
    def __init__(
        self,
        db_repository: "DBRepository",
        redis_repository: "RedisRepository"
    ):
        self.db_repository = db_repository
        self.redis_repository = redis_repository
    
    async def add_view(self, video_id: int):
        return await self.redis_repository.increment(
            video_id=video_id
        )

    async def get_views(self, video_id: int): 
        return await self.redis_repository.get_views(
            video_id=video_id
        )
