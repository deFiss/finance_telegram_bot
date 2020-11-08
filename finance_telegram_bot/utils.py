from telegram import ReplyKeyboardMarkup
from .constants import BACK


def get_submenu_keyboard(buttons):
    buttons += [[BACK]]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
