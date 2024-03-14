import random
import string
from typing import Callable

import httpx
from django.http import HttpRequest, JsonResponse
from django.urls import path

create_random_string: Callable[[int], str] = lambda size: "".join(
    [random.choice(string.ascii_letters) for _ in range(size)]
)


def generate_article_idea(request: HttpRequest) -> JsonResponse:
    content = {
        "title": create_random_string(size=10),
        "description": create_random_string(size=20),
    }
    return JsonResponse(content)


async def get_current_market_state(request: HttpRequest) -> JsonResponse:
    url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=UAH&to_currency=USD&apikey=V2V43QAQ8RILGBOW"

    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(url)
    # await asyncio.sleep(5)
    rate: str = response.json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"]

    return JsonResponse({"rate": rate})


urlpatterns = [
    path(route="generate-article", view=generate_article_idea),
    path(route="market", view=get_current_market_state),
]
