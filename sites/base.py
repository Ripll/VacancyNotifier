import asyncio
import sys
import traceback
from datetime import datetime, timedelta
import httpx
from msg import VacancyMsg
from config import logger, DEFAULT_TIMEOUT, START_TIME, bot
from models.models import Vacancy
from typing import Dict, List


class SiteBase:
    base_url: str
    add_to_url: str
    cities: Dict[str, str]

    settings: Dict[str, List[Dict[str, str]]]

    chat_urls: Dict[str, List[str]] = None

    def __init__(self, settings):
        self.classname = self.__class__.__name__
        self.settings = settings

        self.chat_urls = {}

        self._build_urls()
        logger.info(f"{self.classname} initialized with {self.chat_urls=}")

    async def run_parser(self):
        while True:
            try:
                await self.__parse()
            except:
                logger.info(f"BaseParser: {str(sys.exc_info()[0])} {str(sys.exc_info()[1])}")
            await asyncio.sleep(DEFAULT_TIMEOUT)

    async def __parse(self):
        for chat_id, urls in self.chat_urls.items():
            logger.info(f"Parsing {self.classname} for {chat_id}")
            for url in urls:
                r = await self.__make_request(url)
                if r:
                    for data in self._format_vacancies(r):
                        if not await Vacancy.filter(site=self.classname,
                                                    site_id=data['site_id']):
                            vacancy = await Vacancy.create(site=self.classname, **data)
                            try:
                                msg = VacancyMsg.def_msg(vacancy)
                                logger.info(msg)
                                if datetime.now() - START_TIME > timedelta(minutes=2):
                                    await bot.send_message(chat_id,
                                                           msg,
                                                           parse_mode="html",
                                                           disable_web_page_preview=True)
                            except Exception as e:
                                logger.info("Flood wait.")

    async def __make_request(self, url):
        async with httpx.AsyncClient() as client:
            try:
                logger.info(f"Get new vacancies from {self.classname}")

                r = await client.get(url)
                return r
            except Exception as e:
                logger.error(f"Error in {self.classname} while making request. {traceback.format_exc()}")

    @staticmethod
    def _format_query(query):
        return query

    def _format_city(self, city):
        try:
            return self.cities[city]
        except:
            return city

    def _build_urls(self):
        for channel_id, channel_settings in self.settings.items():
            self.chat_urls[channel_id] = []
            for settings in channel_settings:
                self.chat_urls[channel_id].append(self.base_url +
                                                  self.add_to_url.format(query=self._format_query(settings['query']),
                                                                         city=self._format_city(settings['city'])))

    def _format_vacancies(self, data_from_site) -> List[Dict]:
        pass

    @staticmethod
    def _format_vacancy(item) -> Dict:
        pass
