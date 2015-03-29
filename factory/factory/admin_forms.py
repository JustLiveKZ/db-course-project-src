from django import forms
from django.core.exceptions import ValidationError
from django.db.models import F
from factory.constants import Messages
from factory.models import Purchase, Material, Transaction, Sale


class PurchaseForm(forms.ModelForm):
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        material = self.cleaned_data.get('material')
        if Transaction.get_balance() < quantity * material.price:
            raise ValidationError(Messages.INSUFFICIENT_FUNDS)
        return quantity

    def save(self, commit=True):
        super(PurchaseForm, self).save(commit)
        Transaction.objects.create_purchase_transaction(amount=self.instance.quantity * self.instance.material.price,
                                                        content_object=self.instance)
        self.instance.material.quantity = F('quantity') + self.instance.quantity
        self.instance.material.save()

    class Meta:
        model = Purchase
        fields = ['material', 'quantity', 'employee']


class SaleForm(forms.ModelForm):
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')
        if product.quantity < quantity:
            raise ValidationError(Messages.NOT_ENOUGH_PRODUCTS)
        return quantity

    def save(self, commit=True):
        super(SaleForm, self).save(commit)
        Transaction.objects.create_sale_transaction(amount=self.instance.quantity * self.instance.product.price,
                                                    content_object=self.instance)
        self.instance.product = F('quantity') - self.instance.quantity
        self.instance.product.save()

    class Meta:
        model = Sale
        fields = ['product', 'quantity', 'employee']