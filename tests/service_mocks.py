class RedisRepositoryMocked:
    VIDEO_KEY_TEMPLATE = "video:{video_id}:views"
    UPDATED_KEY_SET = "videos:updated"

    def __init__(self):
        self.store = {}
        self.updated_set = set()

    async def increment(self, video_id: int) -> int:
        key = self.VIDEO_KEY_TEMPLATE.format(video_id=video_id)
        self.store[key] = self.store.get(key, 0) + 1
        self.updated_set.add(video_id)
        return self.store[key]

    async def get_views(self, video_id: int) -> int:
        key = self.VIDEO_KEY_TEMPLATE.format(video_id=video_id)
        return self.store.get(key, 0)
    
    async def _set_views(self, video_id: int, value: int):
        key = self.VIDEO_KEY_TEMPLATE.format(video_id=video_id)
        self.store[key] = value