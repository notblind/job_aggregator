FROM python:3.11
ENV PYTHONUNBUFFERED=1

WORKDIR /vacancies
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /vacancies
EXPOSE 8000