from datetime import datetime, timedelta, date
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from config.utils import get_async_session

from src.models.employee import Employee, EmployeeInfo, Position
from src.core.exceptions import (
    EmployeeInfoNotFoundError,
    EmployeeInfoExistsError,
    PositionNotFoundError,
)
from src.schemas.employee import EmployeeInfoCreate, SalaryResponse

from .base import BaseRepository


class EmployeeRepository(BaseRepository):
    model = EmployeeInfo

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_employee_info(self, employee_id):
        return await self.get_one_by_field("employee_id", employee_id)

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

    async def calculate_salary(self, employee_info: EmployeeInfo):
        position = await self.db.get(Position, employee_info.position_id)
        if not position:
            raise PositionNotFoundError()

        employment_date = employee_info.employment_date
        print(employment_date)
        print(date.today())

        years_employed = (date.today() - employment_date).days // 365
        base_salary = position.base_salary

        salary = base_salary * (1.2**years_employed)

        return salary

    async def get_employee_salary(self, employee: Employee) -> SalaryResponse:
        employee_info = await self.get_employee_info(employee.id)
        if not employee_info:
            raise EmployeeInfoNotFoundError()

        salary = await self.calculate_salary(employee_info)

        employment_year = employee_info.employment_date.year
        current_year = datetime.utcnow().year

        total_increases = current_year - employment_year

        next_increase_date = employee_info.employment_date + timedelta(
            days=365 * total_increases
        )
        days_until_increase = (next_increase_date - date.today()).days

        if days_until_increase < 0:
            next_increase_date += timedelta(days=365)
            days_until_increase = (next_increase_date - date.today()).days

        return SalaryResponse(
            id=employee_info.id,
            first_name=employee_info.first_name,
            last_name=employee_info.last_name,
            birth_year=employee_info.birth_year,
            employment_date=employee_info.employment_date,
            position_id=employee_info.position_id,
            employee_id=str(employee_info.employee_id),
            salary=salary,
            next_increase_date=next_increase_date,
            days_until_increase=days_until_increase,
        )


async def get_employee_info_repository(db: AsyncSession = Depends(get_async_session)):
    return EmployeeRepository(db)
