import os
from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic import SecretStr


@dataclass
class TgBot:
    token: SecretStr
    admin_ids: list[int]


@dataclass
class DbConfig:
    database: str
    user: str
    password: str
    host: str
    port: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def load_config():
    load_dotenv()

    return Config(
        tg_bot=TgBot(
            token=SecretStr(os.getenv('BOT_TOKEN')),
            admin_ids=list(map(int, str(os.getenv('ADMINS')))),
        ),
        db=DbConfig(
            database=str(os.getenv('DATABASE')),
            user=str(os.getenv('USER')),
            password=str(os.getenv('PASSWORD')),
            host=str(os.getenv('HOST')),
            port=str(os.getenv('PORT')),
        )
    )
