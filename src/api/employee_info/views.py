from fastapi import APIRouter, Depends, status

from src.repositories.employee_info import (
    EmployeeInfoRepository,
    get_employee_info_repository,
)
from src.repositories.position import PositionRepository, get_position_repository
from src.schemas.employee_info import EmployeeInfoCreate
from src.models.employee import Employee
from src.api.auth.services import current_active_user
from src.core.exceptions import PositionNotFoundError

router = APIRouter()


@router.post("/info", status_code=status.HTTP_201_CREATED)
async def fill_employee_info(
    employee_info_data: EmployeeInfoCreate,
    employee: Employee = Depends(current_active_user),
    employee_info_repo: EmployeeInfoRepository = Depends(get_employee_info_repository),
    position_repo: PositionRepository = Depends(get_position_repository),
):
    position = await position_repo.get_position_by_id(employee_info_data.position_id)
    if not position:
        raise PositionNotFoundError()

    await employee_info_repo.create_employee_info(employee.id, employee_info_data)
    return {"message": f"Employee info created for {employee.email}."}


@router.put("/info", status_code=status.HTTP_200_OK)
async def update_employee_info(
    employee_info_data: EmployeeInfoCreate,
    employee: Employee = Depends(current_active_user),
    employee_info_repo: EmployeeInfoRepository = Depends(get_employee_info_repository),
):
    await employee_info_repo.update_employee_info(employee_info_data, employee)
    return {"message": f"Employee info updated for {employee.email}."}
