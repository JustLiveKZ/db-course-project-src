from django.db import models
from factory.constants import TransactionTypes


class TransactionManager(models.Manager):
    def create_purchase_transaction(self, **kwargs):
        return self.create(transaction_type=TransactionTypes.PURCHASE, **kwargs)

    def create_sale_transaction(self, **kwargs):
        return self.create(transaction_type=TransactionTypes.SALE, **kwargs)

    def create_salary_transaction(self, **kwargs):
        return self.create(transaction_type=TransactionTypes.SALARY, **kwargs)

    def create_taxes_transaction(self, **kwargs):
        return self.create(transaction_type=TransactionTypes.TAXES, **kwargs)

    def create_investments_transaction(self, **kwargs):
        return self.create(transaction_type=TransactionTypes.INVESTMENTS, **kwargs)