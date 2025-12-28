from typing import TYPE_CHECKING
from httpx import AsyncClient
import pytest

if TYPE_CHECKING:
    from .service_mocks import RedisRepositoryMocked

@pytest.mark.asyncio
async def test_increment_existing_counter(
    async_client: AsyncClient
):
    """
    Проверяем, что существующий счётчик увеличивается корректно.
    """

    video_id = 777
    # Первый инкремент → создаём счётчик
    response = await async_client.post(f"/videos/{video_id}/view")
    assert response.status_code == 200
    data = response.json()
    assert data  == 1
    
    # Второй инкремент → должно увеличиться
    response = await async_client.post(f"/videos/{video_id}/view")
    assert response.status_code == 200
    data = response.json()
    assert data == 2

@pytest.mark.asyncio
async def test_get_counter(
    async_client: AsyncClient,
    redis_repository_mock: "RedisRepositoryMocked"  
):
    
    video_id = 888
    await redis_repository_mock._set_views(888, 789)
    # 
    # Первый инкремент → создаём счётчик
    response = await async_client.get(f"/videos/{video_id}/views")
    assert response.status_code == 200
    data = response.json()
    assert data  == 789

