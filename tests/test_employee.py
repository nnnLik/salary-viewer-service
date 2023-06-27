from datetime import date, datetime, timedelta
from httpx import AsyncClient

import pytest

from sqlalchemy import insert, select, update

from src.models.employee import EmployeeInfo, Position
from tests.conftest import async_session_maker


@pytest.fixture
async def access_token(ac: AsyncClient) -> str:
    response = await ac.post(
        "/auth/jwt/login",
        data={"username": "user@example.com", "password": "string"},
    )
    assert response.status_code == 200
    data = response.json()
    return data["access_token"]


async def test_add_position():
    async with async_session_maker() as session:
        await session.execute(
            insert(Position).values(id=1, name="Back End Developer", base_salary=600)
        )
        await session.execute(
            insert(Position).values(id=2, name="Front End Developer", base_salary=600)
        )
        await session.commit()

        result = await session.execute(select(Position))
        await session.commit()

        positions = result.all()

        assert positions[0][0].id == 1
        assert positions[0][0].name == "Back End Developer"
        assert positions[0][0].base_salary == 600

        assert positions[1][0].id == 2
        assert positions[1][0].name == "Front End Developer"
        assert positions[1][0].base_salary == 600


async def test_fill_employee_info_with_invalid_data(ac: AsyncClient, access_token: str):
    response = await ac.post(
        "/employee/info",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "first_name": "Dude",
            "last_name": "Dude",
            "birth_year": 1990,
            "position_id": 999,
        },
    )
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Position info not found"


async def test_fill_employee_info_with_valid_data(ac: AsyncClient, access_token: str):
    response = await ac.post(
        "/employee/info",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "first_name": "Dude",
            "last_name": "Dude",
            "birth_year": 1990,
            "position_id": 1,
        },
    )
    assert response.status_code == 201

    data = response.json()
    assert "message" in data
    assert data["message"] == "Employee info created for user@example.com."


async def test_update_employee_info_with_invalid_data(
    ac: AsyncClient, access_token: str
):
    response = await ac.put(
        "/employee/info",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "first_name": "Dude2",
            "last_name": "Dude2",
            "birth_year": 1992,
            "position_id": 3,
        },
    )
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Position info not found"


async def test_update_employee_info_with_valid_data(ac: AsyncClient, access_token: str):
    response = await ac.put(
        "/employee/info",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "first_name": "Dude2",
            "last_name": "Dude2",
            "birth_year": 1992,
            "position_id": 2,
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert data["message"] == "Employee info updated for user@example.com."


async def test_get_employee_salary_1(ac: AsyncClient, access_token: str):
    response = await ac.get(
        "/employee/salary",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert "first_name" in data
    assert "last_name" in data
    assert "birth_year" in data
    assert "employment_date" in data
    assert "position" in data
    assert "employee_id" in data
    assert "salary" in data
    assert "next_increase_date" in data
    assert "days_until_increase" in data

    assert isinstance(data["id"], int)
    assert isinstance(data["first_name"], str)
    assert isinstance(data["last_name"], str)
    assert isinstance(data["birth_year"], int)
    assert isinstance(data["employment_date"], str)
    assert isinstance(data["position"], str)
    assert isinstance(data["employee_id"], str)
    assert isinstance(data["salary"], float)
    assert isinstance(data["next_increase_date"], str)
    assert isinstance(data["days_until_increase"], int)

    assert data["id"] == 1
    assert data["first_name"] == "Dude2"
    assert data["last_name"] == "Dude2"
    assert data["birth_year"] == 1992
    assert datetime.strptime(data["employment_date"], "%Y-%m-%d").date() == date.today()
    assert data["position"] == "Front End Developer"
    assert data["salary"] == 600
    assert data["days_until_increase"] == 0

    employment_date = datetime.strptime(data["employment_date"], "%Y-%m-%d").date()
    next_increase_date = datetime.strptime(
        data["next_increase_date"], "%Y-%m-%d"
    ).date()

    assert (next_increase_date - employment_date).days == 0


async def test_get_employee_salary_unauthorized(ac: AsyncClient):
    response = await ac.get("/employee/salary")
    assert response.status_code == 401


async def test_update_employee_info_1():
    async with async_session_maker() as session:
        stmt = (
            update(EmployeeInfo)
            .where(EmployeeInfo.id == 1)
            .values(employment_date=date.today() - timedelta(days=100))
        )
        await session.execute(stmt)
        await session.commit()

        result = await session.execute(select(EmployeeInfo).where(EmployeeInfo.id == 1))
        await session.commit()

        employee_info = result.scalar()

        assert employee_info.id == 1
        assert employee_info.employment_date == date.today() - timedelta(days=100)


async def test_get_employee_salary_2(ac: AsyncClient, access_token: str):
    response = await ac.get(
        "/employee/salary",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert "first_name" in data
    assert "last_name" in data
    assert "birth_year" in data
    assert "employment_date" in data
    assert "position" in data
    assert "employee_id" in data
    assert "salary" in data
    assert "next_increase_date" in data
    assert "days_until_increase" in data

    assert isinstance(data["employment_date"], str)
    assert isinstance(data["salary"], float)
    assert isinstance(data["next_increase_date"], str)
    assert isinstance(data["days_until_increase"], int)

    assert datetime.strptime(
        data["employment_date"], "%Y-%m-%d"
    ).date() == date.today() - timedelta(days=100)
    assert data["salary"] == 600.0
    assert data["days_until_increase"] == 265

    next_increase_date = datetime.strptime(
        data["next_increase_date"], "%Y-%m-%d"
    ).date()

    assert (next_increase_date - date.today()).days == 265


async def test_update_employee_info_2():
    async with async_session_maker() as session:
        stmt = (
            update(EmployeeInfo)
            .where(EmployeeInfo.id == 1)
            .values(employment_date=date.today() - timedelta(days=400))
        )
        await session.execute(stmt)
        await session.commit()

        result = await session.execute(select(EmployeeInfo).where(EmployeeInfo.id == 1))
        await session.commit()

        employee_info = result.scalar()

        assert employee_info.id == 1
        assert employee_info.employment_date == date.today() - timedelta(days=400)


async def test_get_employee_salary_3(ac: AsyncClient, access_token: str):
    response = await ac.get(
        "/employee/salary",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert "first_name" in data
    assert "last_name" in data
    assert "birth_year" in data
    assert "employment_date" in data
    assert "position" in data
    assert "employee_id" in data
    assert "salary" in data
    assert "next_increase_date" in data
    assert "days_until_increase" in data

    assert isinstance(data["employment_date"], str)
    assert isinstance(data["salary"], float)
    assert isinstance(data["next_increase_date"], str)
    assert isinstance(data["days_until_increase"], int)

    assert datetime.strptime(
        data["employment_date"], "%Y-%m-%d"
    ).date() == date.today() - timedelta(days=400)

    assert data["salary"] == 720.0
    assert data["days_until_increase"] == 330

    next_increase_date = datetime.strptime(
        data["next_increase_date"], "%Y-%m-%d"
    ).date()

    assert (next_increase_date - date.today()).days == 330
