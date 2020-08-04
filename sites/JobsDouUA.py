from bs4 import BeautifulSoup, PageElement
from sites.base import SiteBase
from typing import List, Dict
import unicodedata


class JobsDouUA(SiteBase):
    main_url = "https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python"

    def _format_vacancies(self, data_from_site) -> List[Dict]:
        return [self._format_vacancy(i) for i in
                BeautifulSoup(data_from_site.text, 'html.parser').find_all("div", {"class": "vacancy"})]

    @staticmethod
    def _format_vacancy(item: PageElement):
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
