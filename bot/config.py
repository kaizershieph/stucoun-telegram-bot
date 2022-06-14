from dataclasses import dataclass

from environs import Env


@dataclass
class DataBase:
    host: str
    password: str
    user: str
    database: str

@dataclass
class Bot:
    token: str
    admin_ids: list[int]
    group_id: int

@dataclass
class Config:
    database: DataBase
    bot: Bot


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        database=DataBase(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        bot=Bot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            group_id=int(env.str("GROUP_ID"))
        )
    )