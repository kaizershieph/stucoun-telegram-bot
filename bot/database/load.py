from tortoise import Tortoise, run_async


async def init_db():
    
    await Tortoise.init(
        db_url='sqlite://stucoun.db',
        modules={'models': ['bot.database.models']}
    )

    await Tortoise.generate_schemas(safe=True)
    

