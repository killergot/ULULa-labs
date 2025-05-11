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
class Config:
    database: DB
    secret_keys: SecretKeys
    smtp: SMTP






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
                            password=str(env('SMTP_PASS'))))