from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class DBConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 100
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class PrefixConfig(BaseModel):
    api: str = "/api"


class Admin(BaseModel):
    username: str
    password: str
    token: str
    secret: str


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str = "sdsdfaadfnjk;lltxcvbtipwwgifgiojn"
    verification_token_secret: str = "alsfjadfgdddkklofvghnsfdgadfgadfgogn"
    jwt_secret: str = "alsfjadfgdddkklofvghnsfdgadfgadfgogn"


class JWT(BaseModel):
    secret: str = "alsfjadfgdddkklofvghnsfdgadfgadfgogn"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI_CONFIG__",
        env_file=(".env.template", ".env"),
    )
    run: RunConfig = RunConfig()
    prefix: PrefixConfig = PrefixConfig()
    db: DBConfig
    access_token: AccessToken = AccessToken()
    admin: Admin
    jwt: JWT = JWT()


settings = Settings()
