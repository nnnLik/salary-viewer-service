from datetime import datetime
import uuid

from sqlalchemy import (
    TIMESTAMP,
    UUID,
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.generics import GUID
from fastapi_users_db_sqlalchemy import UUID_ID

from .base import Base


class Employee(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "employee"

    id: Mapped[UUID_ID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)
    first_name: str = Column(String(length=255), nullable=True)
    last_name: str = Column(String(length=255), nullable=True)
    birth_year: int = Column(Integer, nullable=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class EmployeeInfo(Base):
    __tablename__ = "employee_info"

    id: int = Column(Integer, primary_key=True, index=True)
    employment_date: int = Column(TIMESTAMP, default=datetime.utcnow)
    social_media: str = Column(String(length=255), nullable=True)
    gitlab_link: str = Column(String(length=255), nullable=True)
    position_id: int = Column(Integer, ForeignKey("position.id"), nullable=True)
    position: Mapped["Position"] = relationship(
        "Position", back_populates="employee_info"
    )
    salary: float = Column(Float, nullable=True)
    experience: int = Column(Integer, nullable=True)

    user_id: UUID = Column(UUID(as_uuid=True), ForeignKey("employee.id"))
    user: Mapped[Employee] = relationship("Employee", back_populates="employee_info")


class Position(Base):
    __tablename__ = "position"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(length=255), nullable=True, unique=True)

    employee_info: Mapped[EmployeeInfo] = relationship(
        "EmployeeInfo", uselist=False, back_populates="position"
    )
