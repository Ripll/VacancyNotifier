import httpx
from bs4 import BeautifulSoup, PageElement
from models import Vacancy
import asyncio
from config import DEFAULT_TIMEOUT
import unicodedata


class WorkUA:
    main_url = "https://www.work.ua/jobs-kyiv-python/"

    async def run_parser(self):
        while True:
            await self.__parse()
            await asyncio.sleep(DEFAULT_TIMEOUT)

    async def __parse(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(self.main_url)
            soup = BeautifulSoup(r.text, 'html.parser')

            for i in soup.find_all("div", {"class": "job-link"}):
                data = self.__format_vacancy(i)
                if not await Vacancy.filter(**data):
                    await Vacancy.create(**data)

    @staticmethod
    def __format_vacancy(item: PageElement):
        data = {
            "site_id": int(item.find_next("a", {"class": "no-decoration"})['href'].split("/")[-2]),
            "title": item.find_next("a").get_text(),
            "company": item.find_next("div", {"class": "add-top-xs"}).find_next("b").get_text(),
            "desc": " ".join(unicodedata.normalize("NFKD", item.find_next("p").get_text()).split()),
            "salary": unicodedata.normalize("NFKD", a) if "грн" in (a := item.find_next("b").get_text()) else None,
            "city": "|".join([i.replace('\xa0', ' ') for i in
                              item.find_next("div", {"class": "add-top-xs"}).get_text().split("·")[1:]]),
            "link": "https://work.ua" + item.find_next("a", {"class": "no-decoration"})['href']

        }
        return data
