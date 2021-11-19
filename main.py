import asyncio
from tortoise import Tortoise
from sites.RobotaUA import RobotaUA
from sites.WorkUA import WorkUA
from sites.DjinniCO import DjinniCO
from sites.JobsDouUA import JobsDouUA
from sites.GrcUA import GrcUA
from sites.RobbyWork import RobbyWork
from config import SETTINGS

loop = asyncio.get_event_loop()


async def run():
    await Tortoise.init(db_url="sqlite://db.sqlite3", modules={"models": ["models.models"]})
    await Tortoise.generate_schemas()

    asyncio.ensure_future(RobotaUA(SETTINGS).run_parser(), loop=loop)
    asyncio.ensure_future(WorkUA(SETTINGS).run_parser(), loop=loop)
    asyncio.ensure_future(DjinniCO(SETTINGS).run_parser(), loop=loop)
    asyncio.ensure_future(JobsDouUA(SETTINGS).run_parser(), loop=loop)
    asyncio.ensure_future(GrcUA(SETTINGS).run_parser(), loop=loop)
    asyncio.ensure_future(RobbyWork(SETTINGS).run_parser(), loop=loop)

loop.create_task(run())
loop.run_forever()
