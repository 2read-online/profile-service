"""Configuration"""
from pydantic import BaseSettings, Field, AnyUrl


class Config(BaseSettings):
    """App configuration"""
    mongodb_url: AnyUrl = Field(
        'mongodb://root:root@mongo:27017',
        description='MongoDB URL with credentials e.g. mongodb:user:pwd@server:port')
    authjwt_secret_key: str = Field('secret', description='Secret key for JWT',
                                    env='SECRET_KEY')


CONFIG = Config()
