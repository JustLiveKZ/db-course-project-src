from django.utils.translation import ugettext as _

INCOME = 1
OUTCOME = 2

TRANSACTION_TYPE_CHOICES = (
    (INCOME, _('Income')),
    (OUTCOME, _('Outcome')),
)