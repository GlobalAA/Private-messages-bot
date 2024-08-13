from aiogram import F, Router
from aiogram.types import CallbackQuery

from database.models import Messages

router = Router()

@router.callback_query(F.data.startswith("w_"))
async def callback_handler(callback: CallbackQuery):
	id = callback.data[2:]

	messages = await Messages.get_or_none(whisper_message_id=id)

	if not messages:
		return await callback.answer("Повідомлення не знайдено")
	
	if messages.for_user == callback.from_user.username:
		return await callback.answer(messages.message, show_alert=True, cache_time=3)

	return await callback.answer("У вас немає доступу до цього повідомлення", cache_time=3)	