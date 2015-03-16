from django import forms
from factory.models import Purchase, Material, Transaction


class PurchaseForm(forms.ModelForm):
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        material = Material.objects.get(self.cleaned_data.get('material'))
        if Transaction.get_balance() < quantity * material:
            pass
        return quantity

    class Meta:
        model = Purchase
        fields = '__all__'