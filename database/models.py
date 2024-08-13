from tortoise import Model, fields


class Messages(Model):
	whisper_message_id = fields.CharField(max_length=32, primary_key=True, generated=False)
	from_user = fields.CharField(max_length=255)
	for_user = fields.CharField(max_length=255)
	message = fields.CharField(max_length=355)