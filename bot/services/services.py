import asyncio
import datetime as dt


def repeatting(hours=0, minutes=0, seconds=0):
    total_seconds = seconds + 60 * minutes + 3600 * hours
    def deco(func):
        async def wrap(*args, **kwargs):
            while True:
                await func(*args, **kwargs)
                await asyncio.sleep(total_seconds)
        return wrap
    return deco

async def wait_to(func, iso_datetime: str):
    aim = dt.datetime.fromisoformat(iso_datetime)
    delay = (aim - dt.datetime.now()).total_seconds()
    await asyncio.sleep(delay=delay)
    await func()




