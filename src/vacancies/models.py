from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declared_attr

from src.database import Base
from src.vacancies.constants import APP_VACANCIES


class BaseVacancies(Base):

    __abstract__ = True
    __table_name__ = ''

    @declared_attr
    def __tablename__(cls):
        return f'{APP_VACANCIES}_{cls.__table_name__}'


class Town(BaseVacancies):
    __table_name__ = 'town'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    id_hh = Column(Integer)


class Currency(BaseVacancies):
    __table_name__ = 'currency'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Schedule(BaseVacancies):
    __table_name__ = 'schedule'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Platform(BaseVacancies):
    __table_name__ = 'platform'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False)


class Vacancy(BaseVacancies):
    __table_name__ = 'vacancy'

    id = Column(Integer, primary_key=True)
    resource_id = Column(Integer)
    platform_id = Column(Integer, ForeignKey(f'{Platform.__tablename__}.id'))
    name = Column(String, nullable=False)
    town_id = Column(Integer, ForeignKey(f'{Town.__tablename__}.id'))
    address = Column(String, nullable=False)

    salary_from = Column(Integer)
    salary_to = Column(Integer)
    currency = Column(Integer, ForeignKey(f'{Currency.__tablename__}.id'))
    gross = Column(Boolean, default=None)

    published_at = Column(DateTime)
    url = Column(String, nullable=False)
    company = Column(String, nullable=False)

    requirement = Column(String, nullable=False)
    responsibility = Column(String, nullable=False)
    schedule = Column(Integer, ForeignKey(f'{Schedule.__tablename__}.id'))

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
