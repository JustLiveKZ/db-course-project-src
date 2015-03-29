from django.utils.translation import ugettext as _

INCOME = 1
OUTCOME = 2

TRANSACTION_TYPE_CHOICES = (
    (INCOME, _('Income')),
    (OUTCOME, _('Outcome')),
)


class ContentTypes:
    PURCHASE = 'purchase'
    SALE = 'sale'
    EMPLOYEE = 'employee'


class TransactionTypes:
    model = None
    _purchase_transaction_type = None
    _purchase_transaction_type_pk = 1
    _sale_transaction_type = None
    _sale_transaction_type_pk = 2
    _salary_transaction_type = None
    _salary_transaction_type_pk = 3
    _taxes_transaction_type = None
    _taxes_transaction_type_pk = 4
    _investments_transaction_type = None
    _investments_transaction_type_pk = 5

    def _load_model(self):
        from factory.models import TransactionType

        self.model = TransactionType

    def _get_transaction_type(self, transaction_type_pk):
        if not self.model:
            self._load_model()
        return self.model.objects.get(pk=transaction_type_pk)

    def _get_purchase_transaction_type(self):
        if self._purchase_transaction_type:
            return self._purchase_transaction_type
        self._purchase_transaction_type = self._get_transaction_type(
            self._purchase_transaction_type_pk)
        return self._purchase_transaction_type

    def _get_sale_transaction_type(self):
        if self._sale_transaction_type:
            return self._sale_transaction_type
        self._sale_transaction_type = self._get_transaction_type(self._sale_transaction_type_pk)
        return self._sale_transaction_type

    def _get_salary_transaction_type(self):
        if self._salary_transaction_type:
            return self._salary_transaction_type
        self._salary_transaction_type = self._get_transaction_type(self._salary_transaction_type_pk)
        return self._salary_transaction_type

    def _get_taxes_transaction_type(self):
        if self._taxes_transaction_type:
            return self._taxes_transaction_type
        self._taxes_transaction_type = self._get_transaction_type(self._taxes_transaction_type_pk)
        return self._taxes_transaction_type

    def _get_investments_transaction_type(self):
        if self._investments_transaction_type:
            return self._investments_transaction_type
        self._investments_transaction_type = self._get_transaction_type(self._investments_transaction_type_pk)
        return self._investments_transaction_type

    PURCHASE = property(_get_purchase_transaction_type)
    SALE = property(_get_sale_transaction_type)
    SALARY = property(_get_salary_transaction_type)
    TAXES = property(_get_taxes_transaction_type)
    INVESTMENTS = property(_get_investments_transaction_type)


class Messages:
    INSUFFICIENT_FUNDS = _('Insufficient Funds')
    NOT_ENOUGH_PRODUCTS = _('Not Enough Products in the Store')