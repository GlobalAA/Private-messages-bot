from aiogram import Router

from .main import router


def setup_routers() -> Router:
	handlers = Router(name="handlers main router")

	handlers.include_router(router)

	return handlers