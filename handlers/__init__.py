from aiogram import Router

from .inline import setup_routers as in_routers
from .main import router


def setup_routers() -> Router:
	handlers = Router(name="handlers main router")

	handlers.include_router(router)
	handlers.include_router(in_routers())

	return handlers