from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, StringCommandHandler
from telegram.ext import Filters
from .filters import AdminWhitelistFilter
from dotenv import load_dotenv
import os
from . import handlers
from .сonversations import AddLossConversation


class Bot:

    def __init__(self):
        load_dotenv()
        self._updater = Updater(token=os.getenv('TELEGRAM_BOT_TOKEN'), use_context=True)
        self._dp = self._updater.dispatcher

        self.add_loss_conversation = AddLossConversation()

    def start(self):
        self._add_handler()
        print(f'{self._updater.bot.name} runing!')
        self._updater.start_polling(poll_interval=1, timeout=40, clean=False)
        # self._updater.idle()

    def _add_handler(self):
        # We do not accept updates from users who are not in the whitelist
        self._dp.add_handler(MessageHandler(AdminWhitelistFilter(), callback=handlers.user_checker))

        self._dp.add_handler(CommandHandler('start', handlers.start))

        self._dp.add_handler(ConversationHandler(
            entry_points=[
                MessageHandler(Filters.regex('🔻 Добавить расход'), callback=self.add_loss_conversation.select_deposit)
            ],
            states={
                'select_type': [CallbackQueryHandler(self.add_loss_conversation.select_type, pattern='loss_deposit.+')],
                'select_amount': [CallbackQueryHandler(self.add_loss_conversation.select_amount, pattern='loss_type_.+')],
                'add_loss': [MessageHandler(Filters.text, callback=self.add_loss_conversation.add_loss)],

            },
            fallbacks=[CommandHandler("start", handlers.start)],
            allow_reentry=True,
        ))