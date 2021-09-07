
from typing import Set, Optional
from pydantic import (
    BaseSettings,
    PyObject,
    RedisDsn,
    PostgresDsn,
    Field
)


class CheckSet(BaseSettings):
    """set data up"""
    secret: Optional[str] = Field( env='ATUSEC')
    log_rod: Optional[int] = Field( env='LOG_H')

class Settings(BaseSettings):
    """"connect to postgres and load data warehouse"""
    
    auth_key: Optional[str]
    api_key: Optional[str] = Field(env='my_api_key')

    redis_dsn: RedisDsn = 'redis://user:pass@localhost:6379/1'
    pg_dsn: PostgresDsn = Field(..., env='PGDB_URI', alias="just_get")

    special_function: PyObject = 'math.cos'

    # to override domains:
    # export my_prefix_domains='["foo.com", "bar.com"]'
    domains: Set[str] = set()

    # to override more_settings:
    # export my_prefix_more_settings='{"foo": "x", "apple": 1}'
    #more_settings: SubModel = SubModel()

    class Config:
        env_prefix = 'my_prefix_'  # defaults to no prefix, i.e. ""
        fields = {
            'auth_key': {
                'env': 'my_auth_key',
            },
            'redis_dsn': {
                'env': ['service_redis_dsn', 'redis_url']
            }
        }