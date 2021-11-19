from bs4 import BeautifulSoup, PageElement
from sites.base import SiteBase
from typing import List, Dict
import unicodedata
import re


class GrcUA(SiteBase):
    base_url = "https://grc.ua/search/vacancy?order_by=publication_time&clusters=true"
    add_to_url = "&area={city}&text={query}&enable_snippets=true"
    cities = {
        "Kyiv": "115"
    }

    def _format_vacancies(self, data_from_site) -> List[Dict]:
        return [self._format_vacancy(i) for i in
                BeautifulSoup(data_from_site.text, 'html.parser').find_all("div", {"class": "vacancy-serp-item"})]

    @staticmethod
    def _format_vacancy(item: PageElement):
        data = {
            "site_id": int(re.findall("\d+", item.find_next("a", {"class": "bloko-link"})['href'])[0]),
            "title": item.find_next("a", {"class": "bloko-link"}).get_text(),
            "company": item.find_next("a", {"data-qa": "vacancy-serp__vacancy-employer"}).get_text(),
            "desc": " ".join(unicodedata.normalize("NFKD",
                                                   item.find_next("div", {"class": "g-user-content"}).get_text()).split()),
            "salary": unicodedata.normalize("NFKD", a.get_text()) if
                                (a := item.find_next("div",
                                                    {"class": "vacancy-serp-item__sidebar"})) else None,
            "city": item.find_next("div", {"data-qa": "vacancy-serp__vacancy-address"}).get_text(),
            "link": item.find_next("a", {"class": "bloko-link"})['href']

        }
        return data
