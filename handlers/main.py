from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router(name="Main Router")

@router.message(CommandStart())
async def start_message(message: Message):
	await message.answer(f"Привіт, це бот, який допоможе тобі анонімно спілкуватися, для того щоб мною користуватися, виклич мене в групі за допомогою @messageprvt_bot ...")