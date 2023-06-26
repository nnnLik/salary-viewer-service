import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from config.settings import settings
from config.logger import Logger
from config.utils import get_employee_db

from src.models.employee import Employee

logger = Logger().logger


class EmployeeManager(UUIDIDMixin, BaseUserManager[Employee, uuid.UUID]):
    reset_password_token_secret = settings.server.SECRET
    verification_token_secret = settings.server.SECRET

    async def on_after_register(
        self, employee: Employee, request: Optional[Request] = None
    ):
        logger.info(f"Employee {employee.id} has registered.")


async def get_user_manager(user_db=Depends(get_employee_db)):
    yield EmployeeManager(user_db)
