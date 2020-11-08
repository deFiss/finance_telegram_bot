from finance_telegram_bot.сonversations.change_deposit.add_income_conversation import AddIncomeConversation
from finance_telegram_bot.сonversations.change_deposit.add_loss_conversation import AddLossConversation
from finance_telegram_bot.сonversations.manage_models.manage_deposits_conversation import ManageDepositsConversation
from .manage_models.manage_deposits_conversation import ManageDepositsConversation
from .manage_models.manage_income_types_conversation import ManageIncomeTypesConversation
from .manage_models.manage_loss_types_conversation import ManageLossTypesConversation

__all__ = [
    'add_loss_conversation',
    'add_income_conversation',

    'manage_deposits_conversation',
    'manage_income_types_conversation',
    'manage_loss_types_conversation'
]

add_loss_conversation = AddLossConversation()
add_income_conversation = AddIncomeConversation()
manage_deposits_conversation = ManageDepositsConversation()
manage_income_types_conversation = ManageIncomeTypesConversation()
manage_loss_types_conversation = ManageLossTypesConversation()
