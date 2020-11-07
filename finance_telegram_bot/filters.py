from telegram.ext import MessageFilter
import os


class AdminWhitelistFilter(MessageFilter):
    name = 'Filters.admin_whitelist_filter'

    def filter(self, message):
        whitelist = os.getenv('USER_ID_WHITELIST').split(',')
        return str(message.from_user.id) not in whitelist