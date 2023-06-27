from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config.utils import get_async_session

from src.models.employee import Position
from src.core.exceptions import PositionNotFoundError
from src.schemas.position import PositionRead

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

    async def get_all_position(self):
        query = select(Position)
        result = await self.db.execute(query)
        positions = result.scalars().all()
        return [
            PositionRead(
                id=position.id, name=position.name, base_salary=position.base_salary
            )
            for position in positions
        ]

    async def create_position(self, position_data):
        position = self.model(**position_data)
        created_position = await self.create(position)
        return PositionRead(
            id=created_position.id,
            name=created_position.name,
            base_salary=created_position.base_salary,
        )

    async def delete_position(self, position_id):
        position = await self.get_by_id(position_id)
        if not position:
            raise PositionNotFoundError()

        await self.delete(position_id)


def get_position_repository(db: AsyncSession = Depends(get_async_session)):
    return PositionRepository(db)
