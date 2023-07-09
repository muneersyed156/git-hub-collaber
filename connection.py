import os,telebot

BOT_TOKEN = os.environ.get('bot_token')

bot = telebot.TeleBot(BOT_TOKEN)