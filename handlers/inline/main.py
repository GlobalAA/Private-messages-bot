from secrets import token_hex

from aiogram import Router
from aiogram.types import (ChosenInlineResult, InlineQuery,
                           InlineQueryResultArticle, InputTextMessageContent,
                           LinkPreviewOptions)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Messages

router = Router(name="Main Router")

@router.inline_query()
async def start_message(iquery: InlineQuery):
	data, username, message = iquery.query, "", ""
	can_send: bool = True

	if data.startswith("@"):
		username = data.split(maxsplit=1)[0]
	if data.count(" ") >= 1:
		message = data[len(username):]
	if len(message) >= 355:
		message = ""
	if not username or not message:
		can_send = False
	
	id = token_hex(16) 

	markup = InlineKeyboardBuilder().button(text="👀 Подивитися", callback_data=f"w_{id}")

	results = [
		InlineQueryResultArticle(
			id=id if can_send else 'error_message', 
			title=f"Формат запроса {username or '<@user>'} {message or '<message>'}",
			description=f"Відправити повідомлення пошепки, яке зможе прочитати лише відмічений користувач",
			input_message_content=InputTextMessageContent(
				message_text=f"Відправлено повідомлення пошепки для <b>{username}</b>" if can_send else "Помилка...",
				link_preview_options=LinkPreviewOptions(is_disabled=True),
				disable_web_page_preview=True
			),
			reply_markup=markup.as_markup() if can_send else None
		)
	]
	
	await iquery.answer(results, is_personal=False)

@router.chosen_inline_result()
async def pagination_demo(chosen_result: ChosenInlineResult):
	result_id = chosen_result.result_id
	if result_id == "error_message":
		return
	
	username, message = chosen_result.query.split(maxsplit=1)
	username = username.replace("@", "")
	from_user = chosen_result.from_user.username or chosen_result.from_user.full_name

	if (msg := await Messages.get_or_none(whisper_message_id=result_id)) != None:
		await msg.update_from_dict({
			'whisper_message_id': result_id,
			'from_user': from_user,
			'for_user': username,
			'message': message
		})
		return await msg.save()

	await Messages.create(whisper_message_id=result_id, from_user=from_user, for_user=username, message=message)