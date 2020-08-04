import httpx
from bs4 import BeautifulSoup, PageElement
from models import Vacancy
import asyncio
from config import DEFAULT_TIMEOUT


class RobotaUA:
    main_url = "https://rabota.ua/jobsearch/vacancy_list?keyWords=python&regionId=1"

    async def run_parser(self):
        while True:
            await self.__parse()
            await asyncio.sleep(DEFAULT_TIMEOUT)

    async def __parse(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(self.main_url)
            soup = BeautifulSoup(r.text, 'html.parser')

            for i in soup.find_all("article", {"class": "card"}):
                data = self.__format_vacancy(i)
                if not await Vacancy.filter(**data):
                    await Vacancy.create(**data)

    @staticmethod
    def __format_vacancy(item: PageElement):
        data = {
            "site_id": int(item["data-vacancy-id"]),
            "title": item.find_next("a", {"class": "ga_listing"}).get_text().replace("\n", ""),
            "company": item.find_next("a", {"class": "company-profile-name"}).get_text(),
            "desc": item.find_next("div", {"class": "card-description"}).get_text(),
            "salary": a if (a := item.find_next("span", {"class": "salary"}).get_text()) else None,
            "city": item.find_next("span", {"class": "location"}).get_text(),
            "link": "https://robota.ua" + item.find_next("a", {"class": "ga_listing"})['href']

        }
        return data

