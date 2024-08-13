from aiogram import Router

from .main import router


def setup_router() -> Router:
	callbacks = Router(name="Callback routers")
	callbacks.include_router(router)

	return callbacks