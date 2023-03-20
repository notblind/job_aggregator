from src.vacancies.constants import PLATFORM_CODES


async def request_vacancy_from_hh(vacancy):
    pass


async def request_vacancy(vacancy):
    if vacancy.platform_id.name != PLATFORM_CODES.HH:
        return await request_vacancy_from_hh(vacancy)
    return
