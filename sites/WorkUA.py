import httpx
from bs4 import BeautifulSoup, PageElement
from models.models import Vacancy
import asyncio
from config import DEFAULT_TIMEOUT, logger
import unicodedata
from sites.base import SiteBase
from typing import List, Dict


class WorkUA(SiteBase):
    main_url = "https://www.work.ua/jobs-kyiv-python/"

    def _format_vacancies(self, data_from_site) -> List[Dict]:
        return [self._format_vacancy(i) for i in
                BeautifulSoup(data_from_site.text, 'html.parser').find_all("div", {"class": "job-link"})]

    @staticmethod
    def _format_vacancy(item: PageElement):
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
