from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str = '127.0.0.1'
    db_port: int = 5432 
    db_user: str = 'postgres'
    db_password: str = 'postgres'
    db_name: str = 'postgres'
    db_schema: str = 'main'
    dd_pool_min_size: int = 5
    db_pool_max_size: int = 20
    redis_host: str = '127.0.0.1'
    redis_port: int = 6379


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)