
# app/repositories/postgres_repo.py
import asyncpg

class DBRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def increment(self, video_id: int, view_count: int) -> int:
        return await self.pool.fetchval(
            """
            INSERT INTO video_views (video_id, views)
            VALUES (:video_id, 1)
            ON CONFLICT (video_id)
            DO UPDATE SET views = video_views.views + 1
            RETURNING views
            """,
            video_id, view_count
        )
    
    async def get_views(self, video_id):
        pass