from .change_deposit.add_income_conversation import AddIncomeConversation
from .change_deposit.add_loss_conversation import AddLossConversation
from .use_template.use_template_conversation import UseTemplateConversation

from .manage_models.manage_deposits_conversation import ManageDepositsConversation
from .manage_models.manage_income_types_conversation import ManageIncomeTypesConversation
from .manage_models.manage_loss_types_conversation import ManageLossTypesConversation
from .manage_models.manage_template_conversation import ManageTemplateConversation

__all__ = [
    'add_loss_conversation',
    'add_income_conversation',
    'use_template_conversation',

    'manage_deposits_conversation',
    'manage_income_types_conversation',
    'manage_loss_types_conversation',
    'manage_template_conversation',
]

add_loss_conversation = AddLossConversation()
add_income_conversation = AddIncomeConversation()
use_template_conversation = UseTemplateConversation()

manage_deposits_conversation = ManageDepositsConversation()
manage_income_types_conversation = ManageIncomeTypesConversation()
manage_loss_types_conversation = ManageLossTypesConversation()
manage_template_conversation = ManageTemplateConversation()