
from typing import Set, Optional
from pydantic import (
    BaseSettings,
    PyObject,
    RedisDsn,
    PostgresDsn,
    DirectoryPath,
    FilePath,
    FileUrl,
    EmailStr,
    NameEmail,
    Field)

class CheckSet(BaseSettings):
    """set data up"""
    secret: str = Field(default=None, env='ATUSEC')
    log_rod: int = Field(default=None, env='LOG_H')
    media_folder: DirectoryPath = Field("/home/johnmba/flaskproject/Account/src/static/test_upload")
    allowed_extension: tuple = Field(default=("MPG", "JPEG", "PNG"), const=True)
    file_size: int = Field(default= 16 * 1024 * 1024, const=True)
    dormain: str = Field(default="questarenz.com", env="DORMAIN")
    quest_mailer: str = Field(default=None, env="FROMAILER")
    quest_pass: str = Field(default=None, env="MAILER_PASSA")
    geop: str = Field(default=None, env="LOCATELI")


class Settings(BaseSettings):
    """"connect to postgres and load data warehouse"""
    
    auth_key: Optional[str]
    api_key: Optional[str] = Field(env='my_api_key')
    #host="localhost", port=6379, db=1, password="j7+jOomYiIP6APPxSBaxR8vcmqjkPnknGN0GHDEmYF3z9ChJ10XkIJPmN5k0ql5PlY60TXiW0AVDQv13@localhost:6379/1"
    redis_dsn: RedisDsn = 'redis://Auth:j7+jOomYiIP6APPxSBaxR8vcmqjkPnknGN0GHDEmYF3z9ChJ10XkIJPmN5k0ql5PlY60TXiW0AVDQv13@localhost:6379/{}'
    pg_dsn: PostgresDsn = Field(..., env='DEV_URI', alias="just_get")
    redis_env_dsn: RedisDsn = Field(..., env="DEV_REDIS", alias="redis_get")

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

if __name__ == "__main__":
    print(CheckSet().dict())