from pydantic import BaseModel


class EmployeeInfoCreate(BaseModel):
    first_name: str
    last_name: str
    birth_year: int
    position_id: int
