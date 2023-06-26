from typing import Optional
import uuid

from pydantic import EmailStr

from fastapi_users import schemas, models


class EmployeeRead(schemas.BaseUser[uuid.UUID]):
    id: models.ID
    first_name: str
    last_name: str
    birth_year: int
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class EmployeeCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    birth_year: int
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class EmployeeUpdate(schemas.BaseUserUpdate):
    password: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]
