import asyncio
from tortoise import Tortoise
from sites.RobotaUA import RobotaUA
from sites.WorkUA import WorkUA
from sites.DjinniCO import DjinniCO
from sites.JobsDouUA import JobsDouUA
from sites.GrcUA import GrcUA

loop = asyncio.get_event_loop()


async def run():
    await Tortoise.init(db_url="sqlite://db.sqlite3", modules={"models": ["models.models"]})
    await Tortoise.generate_schemas()
    asyncio.ensure_future(RobotaUA().run_parser(), loop=loop)
    asyncio.ensure_future(WorkUA().run_parser(), loop=loop)
    asyncio.ensure_future(DjinniCO().run_parser(), loop=loop)
    asyncio.ensure_future(JobsDouUA().run_parser(), loop=loop)
    asyncio.ensure_future(GrcUA().run_parser(), loop=loop)

loop.create_task(run())
loop.run_forever()
