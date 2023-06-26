from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from config.utils import get_async_session

from src.models.employee import Position
from src.core.exceptions import PositionNotFoundError

from .base import BaseRepository


class PositionRepository(BaseRepository):
    model = Position

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_position_by_id(self, position_id):
        position = await self.get_by_id(position_id)
        if not position:
            raise PositionNotFoundError()
        return position


def get_position_repository(db: AsyncSession = Depends(get_async_session)):
    return PositionRepository(db)
