from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_host: str = 'localhost'
    postgres_port: int = 5432 
    postgres_db: str = 'postgres'
    postgres_user: str = 'postgres'
    postgres_password: str = 'postgres'
    postgres_schema: str = 'main'
    postgres_pool_min_size: int = 5
    postgres_pool_max_size: int = 20
    redis_host: str = 'localhost'
    redis_port: int = 6379
    sync_batch_size: int = 1000
    sync_max_retry: int = 10
    sync_interval: int = 5


settings = Settings(
    _env_file='../.env',
    _env_file_encoding='utf-8'
)