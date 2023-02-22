task_serializer = 'json'
result_serializer = 'json'
timezone = 'Europe/Moscow'
enable_utc = True
task_track_started = True

imports = ['src.vacancies.tasks']

beat_schedule = {
    'collect_vacancies_from_hh': {
        'task': 'src.vacancies.tasks.collect_vacancies_from_hh',
        'schedule': 30
    }
}
