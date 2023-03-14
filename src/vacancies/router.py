from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.vacancies.models import Vacancy

router = APIRouter(
    prefix='/vacancies/v1',
    tags=['vacancy'],
)


@router.get('/vacancies')
async def api_vacancies(session: AsyncSession = Depends(get_async_session)):
    query = select(Vacancy)
    result = await session.execute(query)
    return result.all()
