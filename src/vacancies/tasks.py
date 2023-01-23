from src.celery_config import app


@app.task
def collect_vacancies_from_hh():
    pass
