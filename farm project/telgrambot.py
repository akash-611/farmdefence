import motiondetection as md
import waterdetection as wd
from telegram.ext import *
import constants as keys


def start_command(update,context):
    update.message.reply_text('Hello! I am Jarvis, Your assistant')

def help_command(update,context):
    update.message.reply_text('wait right here!')

def messagehandling(update, context):
    text = str(update.message.text).lower()
    if text in ["watercontent", "water level", "waterlevel", "water content"]:
        response = wd.Water_detection()
        update.message.reply_text(response)
if __name__ == "__main__":
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(CommandHandler("help",help_command))
    updater.start_polling()
    updater.idle()
    
