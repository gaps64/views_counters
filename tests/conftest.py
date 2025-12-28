import pytest
from httpx import ASGITransport, AsyncClient

from counters_api.app import app
from counters_api.container import Container
from .service_mocks import RedisRepositoryMocked

@pytest.fixture
def redis_repository_mock():
    return RedisRepositoryMocked()


@pytest.fixture
def test_container(redis_repository_mock):
    container = Container(pg_pool=None, redis=None)
    container.redis_repository.override(redis_repository_mock)
    container.wire(modules=["counters_api.api.api"])
    return container


@pytest.fixture
async def async_client(test_container):
    """
    Асинхронный клиент для тестирования FastAPI.
    """
    app.container = test_container
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client