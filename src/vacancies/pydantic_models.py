from pydantic import BaseModel


class PydanticVacancy(BaseModel):
    resource_id: int = None
    platform_id: int = None
    name: str
    address: str = ''
    salary_from: int = None
    salary_to: int = None
    gross: bool = None
    url: str = ''
    requirement: str = ''
    responsibility: str = ''
    company: str = ''
    town_id: int = None
