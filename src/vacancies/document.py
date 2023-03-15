from src.database import Session
from src.vacancies.constants import SEARCH_FIELDS
from src.vacancies.models import Vacancy


def get_hh_document():
    with Session() as session:
        vacancies = session.query(Vacancy).filter(Vacancy.name != '')
        return [{field: getattr(vacancy, field) for field in SEARCH_FIELDS} for vacancy in vacancies]
