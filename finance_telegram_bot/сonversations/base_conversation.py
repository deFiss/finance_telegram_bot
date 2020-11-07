import os
from finance_telegram_bot.http_sessinon import HttpSession
from telegram import ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


class BaseConversation:
    def __init__(self):
        self.session = HttpSession()
        self.session.headers.update({'Authorization': f'Bearer {os.getenv("BACKEND_HOST_TOKEN")}'})


def send_loading_message(func):
    def wrapper(*args, **kwargs):

        try:
            msg = args[1].callback_query.message
            args[1].callback_query.answer('✅')
        except:
            msg = args[1].message

        message = msg.reply_text('<i>⌛️ Загрузка...</i>', parse_mode='HTML')
        kwargs.update({'loading_msg': message})

        return func(*args, **kwargs)

    return wrapper


def delete_message(func):
    def wrapper(*args, **kwargs):

        try:
            msg = args[1].callback_query.message.delete()
            args[1].callback_query.answer('✅')
        except:
            args[1].message.delete()

        return func(*args, **kwargs)

    return wrapper