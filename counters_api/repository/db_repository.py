
# app/repositories/postgres_repo.py
import asyncpg

class DBRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def increment(self, video_id: int, view_count: int) -> int:
        return await self.pool.fetchval(
            """
            INSERT INTO videos (id, views)
            VALUES (:video_id, 1)
            ON CONFLICT (id)
            DO UPDATE SET views = video_views.views + 1
            RETURNING views
            """,
            video_id, view_count
        )
    
    async def get_video_count(self) -> int:
        return await self.pool.fetchval(
            "SELECT COUNT(*) FROM videos"
        )
    
    async def get_videos_paged(self, limit: int = 0, offset: int = 1000):
        records = await self.pool.fetch(
            "SELECT id, views FROM videos ORDER BY id OFFSET $1 LIMIT $2",
            offset, limit
        )
        return records

    
    async def bulk_update_videos(self, videos_list: list[tuple[int, int]]):
        if not videos_list:
            return
        
        query = """
        INSERT INTO videos (id, views)
        VALUES ($1, $2)
        ON CONFLICT (id)
        DO UPDATE SET views = EXCLUDED.views
        """
        await self.pool.executemany(query, videos_list)
        # async with self.pool.acquire() as conn:
        #     async with conn.transaction():
        #         await conn.executemany(query, videos_list)
        
