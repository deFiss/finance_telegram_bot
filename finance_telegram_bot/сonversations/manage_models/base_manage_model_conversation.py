from finance_telegram_bot.сonversations.base_conversation import *


class BaseManageModelConversation(BaseConversation):

    def __init__(self):
        self.url_path = ''
        self.model_name = ''
        self.json_get_root_key = ''
        self.model_fields_list = []
        super().__init__()

    @send_loading_message
    @delete_message
    def menu(self, update, context, loading_msg):
        response = self.session.get(self.url_path).json()
        btns = []

        for item in response[self.json_get_root_key]:

            btn_text = f'{item["emoji"]} {item["name"]}'
            call_data = f'manage_delete_item_{item["_id"]}'

            btn = InlineKeyboardButton(btn_text, callback_data=call_data)
            btns.append([btn])

        loading_msg.edit_text(
            f'<b>🗑 Нажмите по счёту, что бы удалить его</b>',
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(btns)
        )

        update.message.reply_text(
            f'<b>🔻 Или по кнопке ниже, что бы добавить новый</b>',
            parse_mode='HTML',
            reply_markup=get_submenu_keyboard([[ADD]])
        )

        return 'manage_del_element_or_add_new'

    @delete_message
    def delete_item_request(self, update, context):
        context.user_data['delete_request_item_id'] = update.callback_query.data.split('_')[-1]

        update.callback_query.message.reply_text(
            f'<b>‼️ Введите "Подтверждаю" для удаления</b>',
            parse_mode='HTML',
            reply_markup=get_submenu_keyboard([[]])
        )

        return 'delete_confirmed'

    @send_loading_message
    def delete_confirmed(self, update, context, loading_msg):
        response = self.session.delete(f'{self.url_path}{context.user_data["delete_request_item_id"]}/')

        update.message.reply_text(
            f'<b>♻️ Удалено</b>',
            parse_mode='HTML',
            reply_markup=get_submenu_keyboard([[]])
        )

        loading_msg.delete()

        return 'END'

    def add_item(self, update, context):
        context.user_data[f'manage_new_item_{self.model_fields_list[-1]}'] = update.message.text.replace('_', '')

        data = {}

        for field_name in self.model_fields_list:
            data[field_name] = context.user_data[f'manage_new_item_{field_name}']

        response = self.session.post(self.url_path, data=data)

        if response.status_code == 200:

            update.message.reply_text(
                f'<b>✅ Новый {self.model_name} добавлен</b>',
                parse_mode='HTML',
                reply_markup=get_submenu_keyboard([[]])
            )

        else:
            update.message.reply_text(
                f'<b>❌ Произошла ошбика</b>',
                parse_mode='HTML',
                reply_markup=get_submenu_keyboard([[]])
            )

        return 'END'