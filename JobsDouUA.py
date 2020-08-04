import httpx
from bs4 import BeautifulSoup, PageElement
from models import Vacancy
import asyncio
from config import DEFAULT_TIMEOUT
import unicodedata


class JobsDouUA:
    main_url = "https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python"

    async def run_parser(self):
        while True:
            await self.__parse()
            await asyncio.sleep(DEFAULT_TIMEOUT)

    async def __parse(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(self.main_url)
            soup = BeautifulSoup(r.text, 'html.parser')

            for i in soup.find_all("div", {"class": "vacancy"}):
                data = self.__format_vacancy(i)
                if not await Vacancy.filter(**data):
                    await Vacancy.create(**data)

    @staticmethod
    def __format_vacancy(item: PageElement):
        data = {
            "site_id": int(item["_id"]),
            "title": item.find_next("a", {"class": "vt"}).get_text(),
            "company": item.find_next("a", {"class": "company"}).get_text().replace('\xa0', ''),
            "desc": " ".join(unicodedata.normalize("NFKD",
                                                   item.find_next("div", {"class": "sh-info"}).get_text()).split()),
            "salary": unicodedata.normalize("NFKD", a.get_text()) if
                                            (a := item.find_next("span", {"class": "salary"})) else None,
            "city": item.find_next("span", {"class": "cities"}).get_text(),
            "link": item.find_next("a", {"class": "vt"})['href']

        }
        return data
