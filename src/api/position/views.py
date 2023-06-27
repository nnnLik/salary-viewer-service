from typing import List
from fastapi import APIRouter, Depends, status

from src.schemas.position import PositionCreate, PositionRead
from src.repositories.position import PositionRepository, get_position_repository

router = APIRouter()


@router.get(
    "/positions", status_code=status.HTTP_200_OK, response_model=List[PositionRead]
)
async def get_positions(
    position_repo: PositionRepository = Depends(get_position_repository),
):
    positions = await position_repo.get_all_position()
    return positions


@router.post(
    "/positions", status_code=status.HTTP_201_CREATED, response_model=PositionRead
)
async def create_position(
    position: PositionCreate,
    position_repo: PositionRepository = Depends(get_position_repository),
):
    position_data = position.dict(exclude_unset=True)
    created_position = await position_repo.create_position(position_data)
    return created_position


@router.delete("/positions/{position_id}")
async def delete_position(
    position_id: int,
    position_repo: PositionRepository = Depends(get_position_repository),
):
    await position_repo.delete_position(position_id)
    return {"message": "Position deleted successfully"}
