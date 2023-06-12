from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from elasticsearch import Elasticsearch
from src.database import get_async_session
from src.elasticsearch.client import get_es_client
from src.settings import ELASTIC_INDEX
from src.vacancies.models import Vacancy

router = APIRouter(
    prefix="/vacancies/v1",
    tags=["vacancy"],
)


@router.get("/vacancies")
async def api_vacancies(session: AsyncSession = Depends(get_async_session)):
    query = select(Vacancy)
    result = await session.execute(query)
    return result.all()


@router.get("/vacancies/{item_id}")
async def api_vacancies(
    item_id: int, session: AsyncSession = Depends(get_async_session)
):
    query = select(Vacancy).where(Vacancy.id == item_id)
    result = await session.execute(query)
    if result:
        return result.fetchone()

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Please provide a valid query",
    )


@router.get("/vacancies_es")
async def get_posts_from_elastic(
    query: str = Query(alias="q"),
    es_client: Elasticsearch = Depends(get_es_client),
):
    if not query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a valid query",
        )

    search_query = {
        "multi_match": {
            "query": query,
            "type": "most_fields",
            "operator": "and",
            "fields": [
                "name^3",
                "name.ngrams",
                "address^2",
                "subtitle.ngrams",
            ],
        }
    }

    results = es_client.search(
        index=ELASTIC_INDEX,
        query=search_query,
    )

    return [Vacancy(**hit["_source"]) for hit in results["hits"]["hits"]]
