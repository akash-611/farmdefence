import waterdetection as wd
from telegram.ext import *
import constants as keys


def start_command(update,context):
    update.message.reply_text('Hello! I am Jarvis, Your assistant\nAvailable Commands are:\n\t\t\t\t/watercontent')

def help_command(update,context):
    update.message.reply_text('wait right here!')

def water_content(update,context):
    response = wd.Water_detection()
    update.message.reply_text(response)

def messagehandling(update, context):
    text = str(update.message.text).lower()
    if text:
        update.message.reply_text("available commands are: \n\t /watercontent")
if __name__ == "__main__":
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(CommandHandler("help",help_command))
    dp.add_handler(CommandHandler("watercontent",water_content))
    dp.add_handler(MessageHandler(Filters.text, messagehandling))
    updater.start_polling()
    updater.idle()