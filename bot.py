import logging
from asyncio import run

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from tortoise import Tortoise

from callbacks import setup_router as call_routers
from config import BOT_TOKEN
from handlers import setup_routers as handlers_routers

logging.basicConfig(level=logging.INFO)

bot = Bot(
	BOT_TOKEN,
	default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

async def tortoise_init():
	await Tortoise.init(
		db_url="sqlite://db.sqlite3",
		modules={'models': ['database.models']}
	)

	await Tortoise.generate_schemas()

@dp.startup()
async def on_startup():
	await tortoise_init()

	dp.include_router(handlers_routers())
	dp.include_router(call_routers())
	
	await bot.delete_webhook(drop_pending_updates=True)
	
@dp.shutdown()
async def on_shutdown():
	await Tortoise.close_connections()

async def main():
	await dp.start_polling(bot)

if __name__ == "__main__":
	try:
		run(main())
	except RuntimeError:
		...