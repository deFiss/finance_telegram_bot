from finance_telegram_bot.conversations.base_conversation import *


class UseTemplateConversation(BaseConversation):

    @send_loading_message
    def select_template(self, update, context, loading_msg):
        resp = self.session.get('template/').json()
        btns = []
        for item in resp['data']:
            btn = InlineKeyboardButton(
                f'{item["emoji"]} {item["name"]}',
                callback_data=f'select_template_{item["_id"]}'
            )
            btns.append([btn])

        loading_msg.edit_text(
            f'<b>🧾 Выбирите шаблон</b>',
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(btns)
        )

        return 'use'

    @send_loading_message
    @keyboard_message_handler
    def use(self, update, context, loading_msg):
        template_id = update.callback_query.data.split('_')[-1]
        template = self.session.get(f'template/{template_id}/').json()['data']

        data = {
            'deposit_id': template['deposit'],
            'type_id': template['type'],
            'quantity': template['amount'] * -1,
            'comment': f'Шаблон {template["name"]}'
        }

        if template['amount'] > 0:
            history_url = 'income_history/'
        else:
            history_url = 'loss_history/'

        history_resp = self.session.post(history_url, data=data)

        deposit_info_resp = self.session.get(f'deposit/{template["deposit"]}/').json()['data']
        deposit_current_balance = int(deposit_info_resp['balance'])

        new_balance = deposit_current_balance + template['amount']

        deposit_resp = self.session.put(f'deposit/{template["deposit"]}/', data={'balance': new_balance})

        symbol = deposit_info_resp['symbol']

        if history_resp.status_code == 200 and deposit_resp.status_code == 200:
            if template['amount'] < 0:
                info_msg = f'\n〽 Расход {template["amount"]}{symbol}'
            else:
                info_msg = f'\n💹 Доход +{template["amount"]}{symbol}'

            current_balance_msg = f'\n🏛 Текущий баланс депозита: <b>{new_balance}{symbol}</b>'

            loading_msg.edit_text(
                f'✅ Шаблон {template["name"]} использован\n{info_msg}\n{current_balance_msg}',
                parse_mode='HTML',
            )
        else:
            loading_msg.edit_text('❌')

        return 'END'
