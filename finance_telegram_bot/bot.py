from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler,\
    StringCommandHandler
from telegram.ext import Filters
from .filters import AdminWhitelistFilter
import os
from . import handlers
from .constants import *
from .conversations import *


class Bot:

    def __init__(self):
        self._updater = Updater(token=os.getenv('TELEGRAM_BOT_TOKEN'))
        self._dp = self._updater.dispatcher

    def start(self):
        self._add_handlers()
        print(f'{self._updater.bot.name} runing!')
        self._updater.start_polling(poll_interval=1, timeout=40, clean=False)
        # self._updater.idle()

    def _add_handlers(self):
        # We do not accept updates from users who are not in the whitelist
        self._dp.add_handler(MessageHandler(AdminWhitelistFilter(), callback=handlers.user_checker))

        # start command
        self._dp.add_handler(CommandHandler('start', handlers.start))

        # Button back
        self._dp.add_handler(MessageHandler(Filters.regex(BACK), callback=handlers.start))

        # Deposits list btn
        self._dp.add_handler(MessageHandler(Filters.regex(DEPOSITS), callback=handlers.deposit_list))

        # Options menu
        self._dp.add_handler(MessageHandler(Filters.regex(OPTIONS), callback=handlers.options_menu))

        # Clear dialog btn
        self._dp.add_handler(MessageHandler(Filters.regex(CLEAR_DIALOG), callback=handlers.clear_dialog))

        # Add income conversation handler
        self._add_conversation_handler(
            [MessageHandler(Filters.regex(ADD_INCOME), callback=add_income_conversation.select_deposit)],
            states={
                'select_type': [CallbackQueryHandler(add_income_conversation.select_type, pattern='income_deposit.+')],
                'select_amount': [
                    CallbackQueryHandler(add_income_conversation.select_amount, pattern='income_type_.+')
                ],
                'add_income': [MessageHandler(Filters.text, callback=add_income_conversation.add_income)],

            }
        )

        # Add lose conversation handler
        self._add_conversation_handler(
            [MessageHandler(Filters.regex(ADD_LOSE), callback=add_loss_conversation.select_deposit)],
            {
                'select_type': [CallbackQueryHandler(add_loss_conversation.select_type, pattern='loss_deposit.+')],
                'select_amount': [CallbackQueryHandler(add_loss_conversation.select_amount, pattern='loss_type_.+')],
                'add_loss': [MessageHandler(Filters.text, callback=add_loss_conversation.add_loss)],

            }
        )

        # Use template conversation handler
        self._add_conversation_handler(
            [MessageHandler(Filters.regex(USE_TEMPLATE), callback=use_template_conversation.select_template)],
            {
                'use': [CallbackQueryHandler(use_template_conversation.use, pattern='select_template_.+')],

            }
        )

        # Manage deposit conversation handler
        self._add_manage_model_handler(
            entry_btn_word=MANAGE_DEPOSITS,
            model_conv_obj=manage_deposits_conversation,
            first_data_state=MessageHandler(Filters.regex(ADD), callback=manage_deposits_conversation.balance),
            states={
                'deposit_manage_symbol': [MessageHandler(Filters.regex(r'[0-9]'), callback=manage_deposits_conversation.symbol)],
                'deposit_manage_name': [MessageHandler(Filters.text, callback=manage_deposits_conversation.name)],
                'deposit_manage_emoji': [MessageHandler(Filters.text, callback=manage_deposits_conversation.emoji)],
                'add_item': [MessageHandler(Filters.text, callback=manage_deposits_conversation.add_item)],
            }
        )

        # Manage income types handler
        self._add_manage_model_handler(
            entry_btn_word=MANAGE_INCOME_TYPES,
            model_conv_obj=manage_income_types_conversation,
            first_data_state=MessageHandler(Filters.regex(ADD), callback=manage_income_types_conversation.name),
            states={
                'income_type_manage_emoji': [MessageHandler(Filters.text, callback=manage_income_types_conversation.emoji)],
                'add_item': [MessageHandler(Filters.text, callback=manage_income_types_conversation.add_item)],
            }
        )

        # Manage loss types handler
        self._add_manage_model_handler(
            entry_btn_word=MANAGE_LOSS_TYPES,
            model_conv_obj=manage_loss_types_conversation,
            first_data_state=MessageHandler(Filters.regex(ADD), callback=manage_loss_types_conversation.name),
            states={
                'loss_type_manage_emoji': [MessageHandler(Filters.text, callback=manage_loss_types_conversation.emoji)],
                'add_item': [MessageHandler(Filters.text, callback=manage_loss_types_conversation.add_item)],
            }
        )

        # Manage template handler
        self._add_manage_model_handler(
            entry_btn_word=MANAGE_TEMPLATES,
            model_conv_obj=manage_template_conversation,
            first_data_state=MessageHandler(Filters.regex(ADD), callback=manage_template_conversation.name),
            states={
                'template_manage_emoji': [MessageHandler(Filters.text, callback=manage_template_conversation.emoji)],
                'template_manage_deposit': [MessageHandler(Filters.text, callback=manage_template_conversation.deposit)],
                'template_manage_amount': [
                    CallbackQueryHandler(manage_template_conversation.amount, pattern='manage_template_deposit_.+')
                ],
                'template_manage_type': [MessageHandler(Filters.text, callback=manage_template_conversation.type)],
                'add_item': [
                    CallbackQueryHandler(manage_template_conversation.add_item, pattern='manage_template_type_.+')
                ],
            }
        )

    def _add_conversation_handler(self, entry_points, states):
        self._dp.add_handler(ConversationHandler(
            entry_points=entry_points,
            states=states,
            fallbacks=[],
            allow_reentry=True,
        ))

    def _add_manage_model_handler(self, entry_btn_word, first_data_state, states, model_conv_obj):

        states['manage_del_element_or_add_new'] = [
            CallbackQueryHandler(model_conv_obj.delete_item_request, pattern='manage_delete_item_.+'),
            first_data_state
        ]

        states['delete_confirmed'] = [
            MessageHandler(Filters.regex(r'Подтверждаю'), callback=model_conv_obj.delete_confirmed)
        ]

        self._dp.add_handler(ConversationHandler(
            entry_points=[MessageHandler(Filters.regex(entry_btn_word), callback=model_conv_obj.menu)],
            states=states,
            fallbacks=[],
            allow_reentry=True,
        ))
