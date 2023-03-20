import httpx
from fastapi.logger import logger

from src.vacancies.constants import (HTTPX_KEEP_ALIVE, HTTPX_MAX_CONNECTIONS,
                                     HTTPX_TIMEOUT)


class ClientHttpx:
    httpx_client = None

    @classmethod
    def get_httpx_client(cls):
        if cls.httpx_client is None:
            timeout = httpx.Timeout(timeout=HTTPX_TIMEOUT)
            limits = httpx.Limits(max_keepalive_connections=HTTPX_KEEP_ALIVE, max_connections=HTTPX_MAX_CONNECTIONS)
            cls.httpx_client = httpx.AsyncClient(timeout=timeout, limits=limits, http2=True)

        return cls.httpx_client

    @classmethod
    async def close_httpx_client(cls):
        if cls.httpx_client:
            await cls.httpx_client.close()
            cls.httpx_client = None

    @classmethod
    async def query_url(cls, url):
        client = cls.get_httpx_client()

        try:
            response = await client.post(url)
            if response.status_code != 200:
                return {'ERROR OCCURED' + str(await response.text())}

            json_result = response.json()
        except Exception as e:
            return {'Error': e}

        return json_result


async def client_httpx_start():
    logger.info('Start Httpx client')
    ClientHttpx.get_httpx_client()


async def client_httpx_stop():
    logger.info('Stop Httpx client')
    await ClientHttpx.close_httpx_client()
