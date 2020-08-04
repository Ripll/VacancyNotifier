from typing import Dict, List
from sites.base import SiteBase


class DjinniCO(SiteBase):
    main_url = "https://djinni.co/api/jobs/?offset=0&limit=10&query=Python Kyiv"

    def _format_vacancies(self, data_from_site) -> List[Dict]:
        return [self._format_vacancy(i) for i in data_from_site.json()['results']]

    @staticmethod
    def _format_vacancy(item: Dict):
        data = {
            "site_id": item['id'],
            "title": item['title'],
            "company": item['company_name'],
            "desc": item['long_description'][:400] + "...",
            "city": item['location'],
            "link": "https://djinni.co/jobs2/" + item['slug']

        }
        return data
