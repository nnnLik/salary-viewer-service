from pydantic import BaseModel


class PositionRead(BaseModel):
    id: int
    name: str
    base_salary: float


class PositionCreate(BaseModel):
    id: int
    name: str
    base_salary: float

    class Config:
        orm_mode = True
