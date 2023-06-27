from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, db: AsyncSession, model):
        self.db = db
        self.model = model

    async def get_by_id(self, item_id):
        query = select(self.model).where(self.model.id == item_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_one_by_field(self, field_name, field_value):
        query = select(self.model).where(getattr(self.model, field_name) == field_value)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, item):
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update(self, item):
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def delete(self, item_id):
        query = delete(self.model).where(self.model.id == item_id)
        await self.db.execute(query)
        await self.db.commit()
