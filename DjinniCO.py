import httpx
from bs4 import BeautifulSoup, PageElement
from models import Vacancy
import asyncio
from config import DEFAULT_TIMEOUT
import unicodedata
from typing import Dict

class DjinniCO:
    main_url = "https://djinni.co/api/jobs/?offset=0&limit=10&query=Python Kyiv"

    async def run_parser(self):
        while True:
            await self.__parse()
            await asyncio.sleep(DEFAULT_TIMEOUT)

    async def __parse(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(self.main_url)

            for i in r.json()['results']:
                data = self.__format_vacancy(i)
                if not await Vacancy.filter(**data):
                    await Vacancy.create(**data)

    @staticmethod
    def __format_vacancy(item: Dict):
        data = {
            "site_id": item['id'],
            "title": item['title'],
            "company": item['company_name'],
            "desc": item['long_description'][:400] + "...",
            "city": item['location'],
            "link": "https://djinni.co/jobs2/" + item['slug']

        }
        return data
