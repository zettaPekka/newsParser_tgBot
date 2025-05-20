from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

import os

from .models import Base


load_dotenv()

engine = create_async_engine(os.getenv('DB_PATH'))

async def init_database():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)