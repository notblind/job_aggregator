from src.vacancies.constants import PLATFORM_CODE


async def request_vacancy_from_hh(vacancy):
    pass


async def request_vacancy(vacancy):
    if vacancy.platform_id.name != PLATFORM_CODE.HH:
        return await request_vacancy_from_hh(vacancy)
    return
