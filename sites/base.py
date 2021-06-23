import asyncio
import sys
import httpx
from config import logger, DEFAULT_TIMEOUT
from models.models import Vacancy
from typing import Dict, List

class SiteBase:
    main_url = "https://google.com"

    def __init__(self):
        self.classname = self.__class__.__name__

    async def run_parser(self):
        while True:
            try:
                await self.__parse()
            except:
                logger.info(f"BaseParser: {str(sys.exc_info()[0])} {str(sys.exc_info()[1])}")
            await asyncio.sleep(DEFAULT_TIMEOUT)

    async def __parse(self):
        r = await self.__make_request()
        if r:
            for data in self._format_vacancies(r):
                if not await Vacancy.filter(site=self.classname,
                                            site_id=data['site_id']):
                    await Vacancy.create(site=self.classname, **data)

    async def __make_request(self):
        async with httpx.AsyncClient() as client:
            try:
                logger.info(f"Get new vacancies from {self.classname}")

                r = await client.get(self.main_url)
                return r
            except Exception as e:
                logger.info(f"Error in {self.classname} while making request.")

    def _format_vacancies(self, data_from_site) -> List[Dict]:
        pass

    @staticmethod
    def _format_vacancy(item) -> Dict:
        pass
