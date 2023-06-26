from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from db.models.user_model import User


class RegisterCheck(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        session_maker: sessionmaker = data['session_maker']
        async with session_maker() as session:
            session: AsyncSession
            async with session.begin():
                result = await session.execute(select(User).where(User.user_id == event.from_user.id))
                user = result.one_or_none()

                if user is not None:
                    ...
                else:
                    user = User(
                        user_id=event.from_user.id
                    )
                    await session.merge(user)
                    if isinstance(event, Message):
                        await event.answer('Добро пожаловать!')
                    else:
                        await event.message.answer('Добро пожаловать!')

        return await handler(event, data)
