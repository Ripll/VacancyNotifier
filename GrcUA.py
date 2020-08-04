import httpx
from bs4 import BeautifulSoup, PageElement
from models import Vacancy
import asyncio
from config import DEFAULT_TIMEOUT
import unicodedata
import re

class GrcUA:
    main_url = "https://grc.ua/search/vacancy?" \
               "order_by=publication_time&clusters=true&area=115&text=python&enable_snippets=true"

    async def run_parser(self):
        while True:
            await self.__parse()
            await asyncio.sleep(DEFAULT_TIMEOUT)

    async def __parse(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(self.main_url)
            soup = BeautifulSoup(r.text, 'html.parser')

            for i in soup.find_all("div", {"class": "vacancy-serp-item"}):
                data = self.__format_vacancy(i)
                if not await Vacancy.filter(**data):
                    await Vacancy.create(**data)

    @staticmethod
    def __format_vacancy(item: PageElement):
        data = {
            "site_id": int(re.findall("\d+", item.find_next("a", {"class": "bloko-link"})['href'])[0]),
            "title": item.find_next("a", {"class": "bloko-link"}).get_text(),
            "company": item.find_next("a", {"data-qa": "vacancy-serp__vacancy-employer"}).get_text(),
            "desc": " ".join(unicodedata.normalize("NFKD",
                                                   item.find_next("div", {"class": "g-user-content"}).get_text()).split()),
            "salary": unicodedata.normalize("NFKD", a) if
                                (a := item.find_next("div",
                                                          {"class": "vacancy-serp-item__sidebar"}).get_text()) else None,
            "city": item.find_next("span", {"data-qa": "vacancy-serp__vacancy-address"}).get_text(),
            "link": item.find_next("a", {"class": "bloko-link"})['href']

        }
        return data
