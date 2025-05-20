from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    filter: Mapped[str] = mapped_column(nullable=True)