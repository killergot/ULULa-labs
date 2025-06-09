from dataclasses import dataclass
from typing import Optional

from environs import Env

@dataclass
class DB:
    name : str
    host : str
    user : str
    password : str

@dataclass
class SecretKeys:
    jwt : str
    jwt_refresh : str
    yandex : str

@dataclass
class SMTP:
    user : str
    password : str

@dataclass
class S3:
    key_id: str
    secret: str
    region: str
    bucket_name: str
    endpoint: str

@dataclass
class Config:
    database: DB
    secret_keys: SecretKeys
    smtp: SMTP
    s3: S3


def load_config(path: Optional[str] = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(database = DB(name=env('DB_NAME'),
                          host=env('DB_HOST'),
                          user=env('DB_USER'),
                          password=str(env('DB_PASS'))),
                  secret_keys = SecretKeys(yandex = env('YANDEX_SECRET'),
                          jwt = env('JWT_SECRET'),
                          jwt_refresh = env('JWT_REFRESH_SECRET')),
                  smtp=SMTP(user=env('SMTP_USER'),
                            password=str(env('SMTP_PASS'))),
                  s3=S3(key_id=env('AWS_ACCESS_KEY_ID'),
                        secret=env('AWS_SECRET_ACCESS_KEY'),
                        region=env('AWS_REGION'),
                        bucket_name=env('S3_BUCKET_NAME'),
                        endpoint=env('S3_ENDPOINT_URL')))