from src.main import celery_app


@celery_app.task
def collect_vacancies_from_hh():
    pass
