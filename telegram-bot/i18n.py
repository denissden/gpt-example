from pathlib import Path

from aiogram import Dispatcher
from aiogram.utils.i18n import I18n, FSMI18nMiddleware


static: I18n = None


def setup_middleware(dp: Dispatcher):
    base_dir = Path(__file__).parent
    locales_dir = base_dir / "locales"

    global static
    static = I18n(path=locales_dir, default_locale="en", domain="messages")
    m = FSMI18nMiddleware(static)

    dp.message.middleware(m)
