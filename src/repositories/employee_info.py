from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from config.utils import get_async_session

from src.models.employee import Employee, EmployeeInfo
from src.core.exceptions import EmployeeInfoNotFoundError, EmployeeInfoExistsError
from src.schemas.employee_info import EmployeeInfoCreate

from .base import BaseRepository


class EmployeeInfoRepository(BaseRepository):
    model = EmployeeInfo

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_employee_info(self, employee_id):
        return await self.get_by_id(employee_id)

    async def create_employee_info(self, employee_id, employee_info_data):
        existing_info = await self.get_one_by_field("employee_id", employee_id)
        if existing_info:
            raise EmployeeInfoExistsError()

        employee_info = EmployeeInfo(
            first_name=employee_info_data.first_name,
            last_name=employee_info_data.last_name,
            birth_year=employee_info_data.birth_year,
            position_id=employee_info_data.position_id,
            employee_id=employee_id,
        )

        await self.create(employee_info)

        return employee_info

    async def update_employee_info(
        self, employee_info_data: EmployeeInfoCreate, employee: Employee
    ):
        existing_info = await self.get_one_by_field("employee_id", employee.id)
        if not existing_info:
            raise EmployeeInfoNotFoundError()

        existing_info.first_name = employee_info_data.first_name
        existing_info.last_name = employee_info_data.last_name
        existing_info.birth_year = employee_info_data.birth_year
        existing_info.position_id = employee_info_data.position_id

        await self.session.commit()
        await self.session.refresh(existing_info)


async def get_employee_info_repository(db: AsyncSession = Depends(get_async_session)):
    return EmployeeInfoRepository(db)
