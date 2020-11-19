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

    root_list = []
    list_even = len(buttons_list) % 2 == 0

    index = 0
    while True:
        if (not list_even and index % 3 == 0) or (list_even and index % 3 != 0):
            root_list.append([buttons_list[index]])
            index += 1
        else:
            row = [buttons_list[index], buttons_list[index+1]]
            root_list.append(row)
            index += 2

        if index >= len(buttons_list):
            break

    return InlineKeyboardMarkup(root_list, resize_keyboard=True)