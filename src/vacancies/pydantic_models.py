from typing import Union

from pydantic import BaseModel, validator


class PydanticVacancy(BaseModel):
    resource_id: int = None
    platform_id: int = None
    name: str
    address: Union[str, None] = ""
    salary_from: Union[int, None] = None
    salary_to: Union[int, None] = None
    gross: Union[bool, None] = None
    url: Union[str, None] = ""
    requirement: Union[str, None] = ""
    responsibility: Union[str, None] = ""
    company: Union[str, None] = ""
    town_id: Union[int, None] = None

    class Config:
        validate_assignment = True

    @validator("name", "address", "url", "requirement", "responsibility", "company")
    def str_values(cls, value):
        return value or ""
