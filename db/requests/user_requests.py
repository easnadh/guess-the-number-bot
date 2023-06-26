from sqlalchemy import select, update

from db.base import session_maker
from db.models.user_model import User


async def get_user_attempts(user_id: int) -> int:
    async with session_maker() as session:
        async with session.begin():
            results = await session.execute(select(User.attempts).filter(User.user_id == user_id))
            return results.first()[0]


async def get_user_stats(user_id: int):
    async with session_maker() as session:
        async with session.begin():
            results = await session.execute(select(User.total_games, User.wins)
                                            .filter(User.user_id == user_id))
            return results.first()


async def add_user_total_games(user_id: int):
    async with session_maker() as session:
        async with session.begin():
            await session.execute(update(User)
                                  .values(total_games=User.total_games + 1)
                                  .where(User.user_id == user_id))


async def add_user_wins(user_id: int):
    async with session_maker() as session:
        async with session.begin():
            await session.execute(update(User)
                                  .values(wins=User.wins + 1)
                                  .where(User.user_id == user_id))
