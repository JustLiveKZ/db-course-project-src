from django import forms
from factory.models import Product


class ProductChangeForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())