from django import forms
from django.core.exceptions import ValidationError

from factory.constants import Messages, OUTCOME
from factory.models import Purchase, Transaction, Sale, Manufacture, ComponentOfProduct


class PurchaseForm(forms.ModelForm):
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        material = self.cleaned_data.get('material')
        balance = Transaction.get_balance()
        try:
            if balance < quantity * material.price:
                raise ValidationError(Messages.INSUFFICIENT_FUNDS,
                                      params={'required_money': quantity * material.price, 'current_money': balance})
        except AttributeError:
            pass
        return quantity

    class Meta:
        model = Purchase
        fields = 'material', 'quantity', 'employee'


class SaleForm(forms.ModelForm):
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')
        try:
            if product.quantity < quantity:
                raise ValidationError(Messages.NOT_ENOUGH_PRODUCTS,
                                      params={'current_quantity': product.quantity, 'measure': product.measure})
        except AttributeError:
            pass
        return quantity

    class Meta:
        model = Sale
        fields = 'product', 'quantity', 'employee'


class ManufactureForm(forms.ModelForm):
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')
        errors = []
        for component in product.componentofproduct_set.all():
            if component.material.quantity < quantity * component.quantity:
                errors.append(ValidationError(Messages.NOT_ENOUGH_MATERIAL,
                                              params={'required_quantity': quantity * component.quantity,
                                                      'measure': component.material.measure,
                                                      'material': component.material,
                                                      'current_quantity': component.material.quantity}))
        if errors:
            raise ValidationError(errors)
        return quantity

    class Meta:
        model = Manufacture
        fields = 'product', 'quantity', 'employee'


class TransactionForm(forms.ModelForm):
    def clean_amount(self):
        transaction_type = self.cleaned_data.get('transaction_type')
        amount = self.cleaned_data.get('amount')
        try:
            if transaction_type.type is OUTCOME:
                balance = Transaction.get_balance()
                if balance < amount:
                    raise ValidationError(Messages.INSUFFICIENT_FUNDS,
                                          params={'required_money': amount, 'current_money': balance})
        except AttributeError:
            pass
        return amount

    class Meta:
        model = Transaction
        fields = 'transaction_type', 'amount'