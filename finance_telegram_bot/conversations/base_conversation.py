import os
from finance_telegram_bot.http_sessinon import HttpSession
from telegram import ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from finance_telegram_bot.utils import get_submenu_keyboard, get_beautiful_keyboard
from finance_telegram_bot.constants import *


class BaseConversation:
    def __init__(self):
        self.session = HttpSession()


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


def keyboard_message_handler(func):
    def wrapper(*args, **kwargs):

        args[1].callback_query.answer('✅')
        args[1].callback_query.message.edit_reply_markup()
        return func(*args, **kwargs)

    return wrapper