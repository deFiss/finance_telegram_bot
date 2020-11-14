from .base_manage_model_conversation import BaseManageModelConversation, ReplyKeyboardRemove


class ManageDepositsConversation(BaseManageModelConversation):

    def __init__(self):
        super().__init__()

        self.verbose_model_name = 'счёт'
        self.model_name = 'deposit'
        self.model_fields_list = [
            'balance',
            'symbol',
            'name',
            'emoji'
        ]

    @staticmethod
    def balance(update, context):
        update.message.reply_text(
            f'<b>💴 Введите баланс будущего счёта</b>',
            parse_mode='HTML',
            reply_markup=ReplyKeyboardRemove()
        )

        return 'symbol'

    @staticmethod
    def symbol(update, context):
        context.user_data['manage_new_item_balance'] = update.message.text

        update.message.reply_text(
            f'<b>💲 Введите символ валюты будущего счёта</b>',
            parse_mode='HTML',
        )

        return 'name'

    @staticmethod
    def name(update, context):
        context.user_data['manage_new_item_symbol'] = update.message.text

        update.message.reply_text(
            f'<b>ℹ️ Введите название будущего счёта</b>',
            parse_mode='HTML',
        )

        return 'emoji'

    @staticmethod
    def emoji(update, context):
        context.user_data['manage_new_item_name'] = update.message.text

        update.message.reply_text(
            f'<b>🙂 Введите эмодзи для будущего счёта</b>',
            parse_mode='HTML',
        )

        return 'add_item'
