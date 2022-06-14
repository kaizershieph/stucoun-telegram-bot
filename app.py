import asyncio
import datetime as dt
import logging

from aiogram import executor

from bot.context import dp
from bot.services.coroutines import prepare_wash_timetable, notify_kitchen_duty
from bot.services.services import wait_to

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        filename='logfile.log',
        filemode='w'
    )
    logger.info("Starting up")

    try:
        executor.start_polling(dp, skip_updates=True)
        await asyncio.gather([
            wait_to(prepare_wash_timetable, '2022-06-02 00:00'),
            wait_to(notify_kitchen_duty, '2022-06-01 21:00')
        ]) 

    finally:
        await dp.storage.reset_data()
        await dp.bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down")

