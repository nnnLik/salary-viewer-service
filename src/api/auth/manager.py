import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, exceptions, models, schemas

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

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )

        password = user_dict.pop("password")

        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_employee_db)):
    yield EmployeeManager(user_db)
