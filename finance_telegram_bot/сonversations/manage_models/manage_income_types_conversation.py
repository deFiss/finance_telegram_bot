from .base_manage_model_conversation import BaseManageModelConversation, ReplyKeyboardRemove


class ManageIncomeTypesConversation(BaseManageModelConversation):

    def __init__(self):
        super().__init__()

        self.verbose_model_name = 'тип дохода'
        self.model_name = 'type_of_income'
        self.model_fields_list = [
            'name',
            'emoji'
        ]

    @staticmethod
    def name(update, context):
        update.message.reply_text(
            f'<b>💴 Введите название типа</b>',
            parse_mode='HTML',
            reply_markup=ReplyKeyboardRemove()
        )

        return 'emoji'

    @staticmethod
    def emoji(update, context):
        context.user_data['manage_new_item_name'] = update.message.text

        update.message.reply_text(
            f'<b>🙂 Введите эмодзи для будущего типа</b>',
            parse_mode='HTML',
        )

        return 'add_item'
