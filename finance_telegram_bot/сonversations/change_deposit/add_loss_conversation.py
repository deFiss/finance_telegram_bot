from finance_telegram_bot.сonversations.base_conversation import *


class AddLossConversation(BaseConversation):

    @send_loading_message
    @delete_message
    def select_deposit(self, update, context, loading_msg):
        resp = self.session.get('deposits/').json()
        btns = []
        for item in resp['deposits']:
            btn = InlineKeyboardButton(
                f'{item["emoji"]} {item["name"]}',
                callback_data=f'loss_deposit_{item["symbol"]}_{item["_id"]}'
            )
            btns.append([btn])

        loading_msg.edit_text(
            f'<b>💳 Выбери счёт</b>',
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(btns)
        )

        return 'select_type'

    @send_loading_message
    @delete_message
    def select_type(self, update, context, loading_msg):
        context.user_data['loss_deposit_id'] = update.callback_query.data.split('_')[-1]
        context.user_data['loss_deposit_symbol'] = update.callback_query.data.split('_')[-2]

        resp = self.session.get('types_of_losses/').json()

        btns = []
        for item in resp['types_of_losses']:
            btn = InlineKeyboardButton(f'{item["emoji"]} {item["name"]}', callback_data='loss_type_' + item['_id'])
            btns.append([btn])

        loading_msg.edit_text(
            f'<b>〽️ Выбери тип расхода</b>',
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(btns, resize_keyboard=True)
        )

        return 'select_amount'

    @delete_message
    def select_amount(self, update, context):
        context.user_data['loss_type_id'] = update.callback_query.data.split('_')[-1]

        msg = update.callback_query.message.reply_text(
            f'<b>💴 Напиши сумму и комментарий через пробел, если хочешь</b>',
            parse_mode='HTML',
        )

        context.user_data['loss_amount_info_msg_id'] = msg.message_id

        return 'add_loss'


    @send_loading_message
    @delete_message
    def add_loss(self, update, context, loading_msg):
        context.bot.delete_message(update.message.chat.id, context.user_data['loss_amount_info_msg_id'])

        text = update.message.text

        if len(text.split(' '))>1:
            data = text.split(' ')
            quantity = data[0]
            comment = ' '.join(data[1:])
        else:
            quantity = text
            comment = None

        data = {
            'deposit_id': context.user_data['loss_deposit_id'],
            'type_id': context.user_data['loss_type_id'],
            'quantity': quantity,
            'comment': comment
        }

        history_resp = self.session.post('loss_history/', data=data)

        deposit_info_resp = self.session.get(f'deposits/{context.user_data["loss_deposit_id"]}/').json()
        deposit_current_balance = int(deposit_info_resp['deposit']['balance'])

        new_balance = deposit_current_balance - int(quantity)

        deposit_resp = self.session.put(
            f'deposits/{context.user_data["loss_deposit_id"]}/',
            data={'balance': new_balance}
        )

        symbol = context.user_data['loss_deposit_symbol']

        if history_resp.status_code == 200 and deposit_resp.status_code == 200:
            update.message.reply_text(
                f'✅ Добавлен расход <b>{quantity}{symbol}</b>\n🏛 Текущий баланс депозита: <b>{new_balance}{symbol}</b>',
                parse_mode='HTML',
            )
        else:
            update.message.reply_text('❌')

        return 'END'
