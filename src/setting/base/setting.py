from pydantic import DirectoryPath, Field, ImportString, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class CheckSet(BaseSettings):
    """set data up"""

    secret: str = Field(default=None, alias="ATUSEC")
    log_rod: int = Field(alias="LOG_H")
    media_folder: DirectoryPath = Field("src/static/icon")
    allowed_extension: tuple[str, ...] = Field(default=("MPG", "JPEG", "PNG"))
    file_size: int = Field(default=16 * 1024 * 1024)
    dormain: str = Field(default="dotspot.tech", env="DORMAIN")
    # quest_mailer: str = Field(alias="FROMAILER")
    quest_pass: str = Field(default=None, alias="MAILER_PASSA")
    geop: str = Field(default=None, alias="LOCATELI")


class Settings(BaseSettings):
    """ "connect to postgres and load data warehouse"""

    auth_key: str | None
    api_key: str | None = Field(env="my_api_key")
    # host="localhost", port=6379, db=1, password="j7+jOomYiIP6APPxSBaxR8
    # vcmqjkPnknGN0GHDEmYF3z9ChJ10XkIJPmN5k0ql5PlY60TXiW0AVDQv13@localhost:6379/1"
    redis_dsn: RedisDsn = "redis://Auth:j7+jOomYiIP6APPxSBaxR8vcmqjkPnknGN0\
    GHDEmYF3z9ChJ10XkIJPmN5k0ql5PlY60TXiW0AVDQv13@localhost:6379/{}"
    pg_dsn: PostgresDsn = Field(..., env="DEV_URI", alias="just_get")
    redis_env_dsn: RedisDsn = Field(..., env="DEV_REDIS", alias="redis_get")

    special_function: ImportString = "math.cos"

    # to override domains:
    # export my_prefix_domains='["foo.com", "bar.com"]'
    domains: set[str] = set()

    # to override more_settings:
    # export my_prefix_more_settings='{"foo": "x", "apple": 1}'
    # more_settings: SubModel = SubModel()

    class Config:
        env_prefix = "my_prefix_"  # defaults to no prefix, i.e. ""
        fields = {
            "auth_key": {
                "env": "my_auth_key",
            },
            "redis_dsn": {"env": ["service_redis_dsn", "redis_url"]},
        }


if __name__ == "__main__":
    print(CheckSet().model_dump())
