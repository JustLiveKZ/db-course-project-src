from django.db import models
from factory.constants import TransactionTypes


class TransactionManager(models.Manager):
    def create_purchase_transaction(self, **kwargs):
        return self.create(transaction_type=TransactionTypes.get_purchase_transaction_type(), **kwargs)

    def create_sale_transaction(self, **kwargs):
        return self.create(transaction_type=TransactionTypes.get_sale_transaction_type(), **kwargs)

    def create_salary_transaction(self, **kwargs):
        return self.create(transaction_type=TransactionTypes.get_salary_transaction_type(), **kwargs)

    def create_taxes_transaction(self, **kwargs):
        return self.create(transaction_type=TransactionTypes.get_taxes_transaction_type(), **kwargs)

    def create_investments_transaction(self, **kwargs):
        return self.create(transaction_type=TransactionTypes.get_investments_transaction_type(), **kwargs)