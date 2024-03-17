from telegram.ext import Updater
from handlers import *

def main() -> None:
    updater = Updater(telegram_api_key)
    dp = updater.dispatcher
    setup_handlers(dp)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()