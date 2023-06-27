from pydantic import BaseModel
from datetime import date
from typing import Optional


class EmployeeInfoCreate(BaseModel):
    first_name: str
    last_name: str
    birth_year: int
    position_id: int


class SalaryResponse(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    birth_year: Optional[int]
    employment_date: date
    position: Optional[str]
    employee_id: str
    salary: float
    next_increase_date: Optional[date]
    days_until_increase: Optional[int]
