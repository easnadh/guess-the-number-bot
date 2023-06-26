from sqlalchemy import Column, Integer

from db.base import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    total_games = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    attempts = Column(Integer, default=3)
