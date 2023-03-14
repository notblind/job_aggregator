from fastapi import APIRouter

router = APIRouter(
    prefix='/vacancies/v1',
    tags=['vacancy'],
)


@router.get('/vacancies')
async def api_vacancies():
    return
