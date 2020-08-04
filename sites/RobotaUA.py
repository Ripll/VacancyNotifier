from bs4 import BeautifulSoup, PageElement
from sites.base import SiteBase
from typing import List, Dict


class RobotaUA(SiteBase):
    main_url = "https://rabota.ua/jobsearch/vacancy_list?keyWords=python&regionId=1"

    def _format_vacancies(self, data_from_site) -> List[Dict]:
        return [self._format_vacancy(i) for i in
                BeautifulSoup(data_from_site.text, 'html.parser').find_all("article", {"class": "card"})]

    @staticmethod
    def _format_vacancy(item: PageElement):
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

