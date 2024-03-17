from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext,CallbackQueryHandler
from callbacks import *
from device import *
def setup_handlers(dp):
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(select_device,pattern='select_device'))
    dp.add_handler(CallbackQueryHandler(confirm_device,pattern='confirm_device'))
    dp.add_handler(CallbackQueryHandler(ask_more,pattern='askmemore'))
    dp.add_handler(CallbackQueryHandler(audio_response,pattern='audio_response'))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command & ~Filters.update.edited_message, handle_device_name))
    dp.add_handler(CallbackQueryHandler(button_click))
    dp.add_handler(MessageHandler(Filters.voice, process_voice))
