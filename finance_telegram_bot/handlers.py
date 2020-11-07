import os
from telegram import ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup


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
        ['💹 Добавить доход'],
        ['🔻 Добавить расход'],
        ['🏦 Счета', '⚙️ Опции'],
    ]

    update.message.reply_text(
        f'<b>Привет, @{update.message.from_user.username}</b>',
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True)
    )
