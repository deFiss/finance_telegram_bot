from .base_manage_model_conversation import *


class ManageTemplateConversation(BaseManageModelConversation):

    def __init__(self):
        super().__init__()

        self.verbose_model_name = 'шаблон'
        self.model_name = 'template'
        self.model_fields_list = [
            'name',
            'emoji',
            'deposit',
            'amount',
            'type'
        ]

    @staticmethod
    def name(update, context):
        update.message.reply_text(
            f'<b>ℹ️ Введите название будущего шаблона</b>',
            parse_mode='HTML',
            reply_markup=ReplyKeyboardRemove()
        )

        return 'template_manage_emoji'

    @staticmethod
    def emoji(update, context):
        context.user_data['manage_new_item_name'] = update.message.text

        update.message.reply_text(
            f'<b>🙂 Введите эмодзи для будущего шаблона</b>',
            parse_mode='HTML',
        )

        return 'template_manage_deposit'

    def deposit(self, update, context):
        context.user_data['manage_new_item_emoji'] = update.message.text.replace('_', '')

        resp = self.session.get('deposit/').json()
        btns = []
        for item in resp['data']:
            btn = InlineKeyboardButton(
                f'{item["emoji"]} {item["name"]}',
                callback_data=f'manage_template_deposit_{item["_id"]}'
            )
            btns.append(btn)

        update.message.reply_text(
            f'<b>🏛 Выбирите счёт для будущего шаблона</b>',
            parse_mode='HTML',
            reply_markup=get_beautiful_keyboard(btns)
        )

        return 'template_manage_amount'

    @keyboard_message_handler
    def amount(self, update, context):
        context.user_data['manage_new_item_deposit'] = update.callback_query.data.split('_')[-1]

        update.callback_query.message.reply_text(
            f'<b>🔸 Введите положительную или отрицательную сумму</b>',
            parse_mode='HTML',
        )

        return 'template_manage_type'

    def type(self, update, context):
        context.user_data['manage_new_item_amount'] = update.message.text

        if context.user_data['manage_new_item_amount'][0] != '-':
            msg_text = '<b>💹 Выбирите источник дохода</b>'
            url = 'type_of_income/'
        else:
            msg_text = '<b>〽 Выбирите источник расхода</b>'
            url = 'type_of_loss/'

        resp = self.session.get(url).json()
        btns = []
        for item in resp['data']:
            btn = InlineKeyboardButton(
                f'{item["emoji"]} {item["name"]}',
                callback_data=f'manage_template_type_{item["_id"]}'
            )
            btns.append(btn)

        update.message.reply_text(
            msg_text,
            parse_mode='HTML',
            reply_markup=get_beautiful_keyboard(btns)
        )

        return 'add_item'
