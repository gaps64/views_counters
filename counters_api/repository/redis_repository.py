from redis.asyncio import Redis

class RedisRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def increment(self, video_id: int) -> int:
        return await self.redis.incr(f"video:{video_id}:views")
    
    async def get_views(self, video_id: int) -> int:
        return await self.redis.get(f"video:{video_id}:views")
    