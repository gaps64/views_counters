from unittest import result
from redis.asyncio import Redis

class RedisRepository:

    VIDEO_KEY_TEMPLATE = "video:{video_id}:views"
    UPDATED_KEY_SET = "videos:updated"

    def __init__(self, redis: Redis):
        self.redis = redis

    async def increment(self, video_id: int) -> int:
        async with self.redis.pipeline(transaction=True) as pipe:
            pipe.incr(
                self.VIDEO_KEY_TEMPLATE.format(video_id=video_id)
            )
            pipe.sadd(self.UPDATED_KEY_SET, video_id)
            result = await pipe.execute()
            return result[0]

    async def get_views(self, video_id: int) -> int:
        return await self.redis.get(
            self.VIDEO_KEY_TEMPLATE.format(video_id=video_id)
        )
    async def get_updated_videos_count(self) -> int:
        return await self.redis.scard(self.UPDATED_KEY_SET)
    
    async def get_updated_videos_ids(self, max_keys: int = 1000) -> list[int]:
        result =  await self.redis.spop(self.UPDATED_KEY_SET, max_keys) 
        return [int(vid) for vid in result]

    async def get_bulk_video_views(self, video_ids: list[int]) -> dict[int, int]:
        """
        Docstring for get_bulk_video_views
        
        :param video_ids: Description
        :type video_ids: list[int]
        :return: Mapping video_id: views_count
        :rtype: dict[int, int]
        """
        keys = [
            self.VIDEO_KEY_TEMPLATE.format(video_id=vid) for vid in video_ids
        ]
        values = await self.redis.mget(*keys)
        views = [int(vid) for vid in values]
        return list(zip(video_ids, views))
    
    async def set_bulk_videos_views(self, batch = list[tuple[int, int]]):
        mset_dict = {
            self.VIDEO_KEY_TEMPLATE.format(video_id=vid): views for vid, views in batch
        }                        
        await self.redis.mset(mset_dict)
    