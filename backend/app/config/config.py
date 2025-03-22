from dataclasses import dataclass
from typing import Optional

from environs import Env

@dataclass
class DB:
    DB_NAME : str
    DB_HOST : str
    DB_USER : str
    DB_PASS : str


@dataclass
class Config:
    database: DB
    yandex_secret: str




def load_config(path: Optional[str] = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(database = DB(DB_NAME=env('DB_NAME'),
                          DB_HOST=env('DB_HOST'),
                          DB_USER=env('DB_USER'),
                          DB_PASS=str(env('DB_PASS'))),
                  yandex_secret = env('YANDEX_SECRET'))