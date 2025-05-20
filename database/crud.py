from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm.attributes import flag_modified

from  database.models import User
from database.init_db import engine


session_factory = async_sessionmaker(engine)


async def create_user_if_not_exists(user_id: int):
    async with session_factory() as session:
        user = await session.get(User, user_id)
        if not user:
            user = User(user_id=user_id)
            session.add(user)
            await session.commit()


async def set_filter(user_id: int, filter_name: str):
    async with session_factory() as session:
        user = await session.get(User, user_id)
        if not user:
            user = User(user_id=user_id)
            session.add(user)
        user.filter = filter_name
        await session.commit()


async def get_filter(user_id: int):
    async with session_factory() as session:
        user = await session.get(User, user_id)
        if not user:
            user = User(user_id=user_id)
            session.add(user)
        return user.filter