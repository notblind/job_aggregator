import logging

import requests
from fastapi import status
from requests.exceptions import ConnectionError, HTTPError

_logger = logging.getLogger(__name__)


class ExternalApi:

    DEFAULT_API_TIMEOUT = 300
    DEFAULT_PAGE_NAME = "page"
    DEFAULT_OFFSET_NAME = "offset"

    def make_request(self, method, url, params=None, headers=None):
        if not params:
            params = {}
        if not headers:
            headers = {}

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                timeout=self.DEFAULT_API_TIMEOUT,
            )
            response.raise_for_status()
        except ConnectionError:
            text_error = f"Error occurred while making request {method} {url}"
            _logger.error(text_error)
            raise ConnectionError(text_error)

        if response.status_code != status.HTTP_200_OK:
            text_error = f"Error occurred while making request {method} {url}"
            _logger.error(text_error)
            raise HTTPError(text_error)

        return response.json()

    def get_paginated_data(self, method, url, params=None, headers=None):
        if not params:
            params = {}
        page = 1
        while page:
            params[self.DEFAULT_PAGE_NAME] = page
            response = self.make_request(method, url, params, headers)
            yield response
            page = self.get_next_page(page, response)

    def get_next_page(self, page, response):
        raise NotImplementedError("Please Implement this method")
