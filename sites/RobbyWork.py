from sites.base import SiteBase
from typing import List, Dict


class RobbyWork(SiteBase):
    base_url = "https://api.robby.work/api/vacancies?"
    add_to_url = "technologies[0]=3&city_id[0]=1&page=1"

    def _format_vacancies(self, data_from_site) -> List[Dict]:
        return [self._format_vacancy(i) for i in data_from_site.json()['data']]

    @staticmethod
    def _format_vacancy(item: Dict):
        data = {
            "site_id": int(item["id"]),
            "title": item["name"] if item["name"] else "<Title not found>",
            "company": item["company"]["name"],
            "desc": item["short_description"],
            "salary": item["salary"],
            "city": "Kyiv",
            "link": "https://robby.work/ua/vacancies/" + item["slug"]

        }
        return data
