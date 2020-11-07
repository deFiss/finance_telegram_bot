from telegram.ext import BaseFilter
import os


class AdminWhitelistFilter(BaseFilter):
    name = 'Filters.admin_whitelist_filter'

    def filter(self, message):
        whitelist = os.getenv('USER_ID_WHITELIST').split(',')
        return str(message.from_user.id) not in whitelist