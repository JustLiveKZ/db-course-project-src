from django.utils.decorators import classonlymethod
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

    @classonlymethod
    def get_choices_for_field(cls):
        return {'model__in': (cls.PURCHASE, cls.EMPLOYEE, cls.SALE)}


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

    @classonlymethod
    def _load_model(cls):
        from factory.models import TransactionType

        cls.model = TransactionType

    @classonlymethod
    def _get_transaction_type(cls, transaction_type_pk):
        if not cls.model:
            cls._load_model()
        return cls.model.objects.get(pk=transaction_type_pk)

    @classonlymethod
    def get_purchase_transaction_type(cls):
        if cls._purchase_transaction_type:
            return cls._purchase_transaction_type
        cls._purchase_transaction_type = cls._get_transaction_type(
            cls._purchase_transaction_type_pk)
        return cls._purchase_transaction_type

    @classonlymethod
    def get_sale_transaction_type(cls):
        if cls._sale_transaction_type:
            return cls._sale_transaction_type
        cls._sale_transaction_type = cls._get_transaction_type(cls._sale_transaction_type_pk)
        return cls._sale_transaction_type

    @classonlymethod
    def get_salary_transaction_type(cls):
        if cls._salary_transaction_type:
            return cls._salary_transaction_type
        cls._salary_transaction_type = cls._get_transaction_type(cls._salary_transaction_type_pk)
        return cls._salary_transaction_type

    @classonlymethod
    def get_taxes_transaction_type(cls):
        if cls._taxes_transaction_type:
            return cls._taxes_transaction_type
        cls._taxes_transaction_type = cls._get_transaction_type(cls._taxes_transaction_type_pk)
        return cls._taxes_transaction_type

    @classonlymethod
    def get_investments_transaction_type(cls):
        if cls._investments_transaction_type:
            return cls._investments_transaction_type
        cls._investments_transaction_type = cls._get_transaction_type(cls._investments_transaction_type_pk)
        return cls._investments_transaction_type

    @classonlymethod
    def get_choices_for_field(cls):
        return {'pk__in': (cls.get_salary_transaction_type().pk, cls.get_taxes_transaction_type().pk, cls.get_investments_transaction_type().pk)}


class Messages:
    INSUFFICIENT_FUNDS = _('Insufficient funds, %(required_money).2f required while there are only %(current_money).2f')
    NOT_ENOUGH_PRODUCTS = _('Not enough products at the stock, there are only %(current_quantity)s %(measure)s at the stock')
    NOT_ENOUGH_MATERIAL = _('%(required_quantity)s %(measure)s of %(material)s required while there are only %(current_quantity)s %(measure)s')