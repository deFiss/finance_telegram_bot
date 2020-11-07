import os
from telegram import ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup
from .constants import *
from .http_sessinon import HttpSession


def user_checker(update, context):
    admin_id_list = os.getenv('USER_ID_WHITELIST').split(',')

    msg = f"""
💭 <b>Написал какой то пользователь:</b>\n\r
🔹 <b>username</b>: @{update.message.from_user.username}
🔸 <b>id</b>: <code>{update.message.from_user.id}</code>
🔹 <b>first_name</b>: <code>{update.message.from_user.first_name}</code>
🔸 <b>last_name</b>: <code>{update.message.from_user.last_name}</code>
🔹 <b>language_code</b>: <code>{update.message.from_user.language_code}</code>

🔶 <b>Message</b>: \n\r{update.message.text}
    """

    for admin_id in admin_id_list:
        try:
            context.bot.send_message(admin_id, msg, parse_mode='HTML')
        except:
            pass


def start(update, context):
    btns = [
        [ADD_INCOME],
        [ADD_LOSE],
        [DEPOSITS, '⚙️ Опции'],
        [CLEAR_DIALOG]
    ]

    update.message.reply_text(
        f'<b>Привет, @{update.message.from_user.username}</b>',
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True)
    )


def clear_dialog(update, context):
    chat_id = update.message.chat.id

    current_msg_id = update.message.message_id

    for i in range(current_msg_id-50, current_msg_id+1):
        try:
            context.bot.delete_message(chat_id, i)
        except:
            pass

    start(update, context)


def deposit_list(update, context):
    loading_msg = update.message.reply_text('<i>⌛️ Загрузка...</i>', parse_mode='HTML')

    resp = HttpSession().get('deposits/').json()

    msg_text = ''
    for i in resp['deposits']:
        msg_text += f'{i["emoji"]} <b>{i["name"]}</b>  <code>{i["balance"]}{i["symbol"]}</code>\n'

    loading_msg.edit_text(
        msg_text,
        parse_mode='HTML',
    )