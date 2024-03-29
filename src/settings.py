import os

from dotenv import load_dotenv

load_dotenv()


# Database
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

# Redis
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_DB = os.environ.get("REDIS_DB")

# Elasticsearch
ELASTIC_URL = os.environ.get("ELASTIC_URL")
ELASTIC_INDEX = os.environ.get("ELASTIC_INDEX")
