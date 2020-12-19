from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup
from .constants import BACK


def get_submenu_keyboard(buttons):
    buttons += [[BACK]]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def clear_dialog(update, context):
    chat_id = update.message.chat.id
    current_msg_id = update.message.message_id

    error_count = 0
    while error_count < 5:
        try:
            context.bot.delete_message(chat_id, current_msg_id)
            current_msg_id -= 1
        except:
            current_msg_id -= 1
            error_count += 1


def get_beautiful_keyboard(buttons_list):
    if len(buttons_list) == 0:
        return InlineKeyboardMarkup([])
    element_in_row = 2
    root_list = [buttons_list[x:element_in_row+x] for x in range(0, len(buttons_list), element_in_row)]

    return InlineKeyboardMarkup(root_list, resize_keyboard=True)
