from tortoise.models import Model
from tortoise import fields, BaseDBAsyncClient
from typing import List, Optional, Type
from tortoise.signals import post_delete, post_save, pre_delete, pre_save
from config import bot, CHAT_ID
from msg import VacancyMsg


class Vacancy(Model):
    id = fields.IntField(pk=True)
    site_id = fields.IntField()
    title = fields.CharField(max_length=255)
    company = fields.CharField(max_length=50)
    desc = fields.TextField()
    city = fields.CharField(max_length=50)
    salary = fields.CharField(max_length=50, null=True)
    link = fields.TextField()

    def __str__(self):
        return f"{self.title}\n{self.link}"


@post_save(Vacancy)
async def signal_post_save(
    sender: "Type[Vacancy]",
    instance: Vacancy,
    created: bool,
    using_db: "Optional[BaseDBAsyncClient]",
    update_fields: List[str],
) -> None:
    msg = VacancyMsg.def_msg(instance)
    await bot.send_message(CHAT_ID, msg, parse_mode="html", disable_web_page_preview=True)
