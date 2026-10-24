import logging
import os

import requests

logger = logging.getLogger(__name__)

WAREHOUSE_URL = os.getenv(
    "WAREHOUSE_URL", "http://127.0.0.1:8001"
)


def get_book_stock(book_id, access_token):
    """Получить остаток книги из Warehouse."""
    url = f"{WAREHOUSE_URL}/api/stocks/"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(
            url,
            headers=headers,
            params={"book_id": book_id},
            timeout=5,
        )
        response.raise_for_status()

        stocks = response.json()
        for stock in stocks:
            if stock["book_id"] == book_id:
                return stock["quantity"]

        return 0

    except (requests.RequestException, ValueError, KeyError, TypeError):
        logger.exception(
            "Warehouse API request failed for book %s", book_id
        )
        return None