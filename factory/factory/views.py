from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from factory.admin_forms import PurchaseForm, ManufactureForm, SaleForm
from factory.constants import Messages
from factory.forms import ProductChangeForm
from factory.models import Transaction, Product


class ProductMixin(object):
    def get_product(self):
        product_pk = self.request.session.get('product_pk', None)
        try:
            product = Product.objects.get(pk=product_pk)
        except Product.DoesNotExist:
            product = None
        return product


class HomeView(TemplateView, ProductMixin):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['product'] = self.get_product()
        context['purchase_form'] = PurchaseForm()
        context['manufacture_form'] = ManufactureForm(initial={'product': context['product']})
        context['sale_form'] = SaleForm()
        context['product_change_form'] = ProductChangeForm(initial={'product': context['product']})
        context['balance'] = Transaction.get_balance()
        return context


class ProductPartialView(TemplateView, ProductMixin):
    template_name = 'partial/product.html'

    def get_context_data(self, **kwargs):
        self.request.session['product_pk'] = self.kwargs.pop('pk')
        context = super(ProductPartialView, self).get_context_data(**kwargs)
        context['product'] = self.get_product()
        context['manufacture_form'] = ManufactureForm(initial={'product': context['product']})
        return context


class PurchaseView(View):
    def post(self, request, *args, **kwargs):
        purchase_form = PurchaseForm(self.request.POST)
        if purchase_form.is_valid():
            purchase = purchase_form.save()
            purchase.save_related()
            messages.success(self.request, Messages.SUCCESSFUL_PURCHASE % {
                'quantity': purchase.quantity,
                'measure': purchase.material.measure,
                'material': purchase.material
            })
        else:
            messages.error(self.request, Messages.UNSUCCESSFUL_PURCHASE)
        return redirect('factory:home')


class ManufactureView(View, ProductMixin):
    def post(self, request, *args, **kwargs):
        manufacture_form = ManufactureForm(self.request.POST, initial={'product': self.get_product()})
        if manufacture_form.is_valid():
            manufacture = manufacture_form.save()
            manufacture.save_related()
            messages.success(self.request, Messages.SUCCESSFUL_MANUFACTURE % {
                'quantity': manufacture.quantity,
                'measure': manufacture.product.measure,
                'product': manufacture.product
            })
        else:
            messages.error(self.request, Messages.UNSUCCESSFUL_MANUFACTURE)
        return redirect('factory:home')


class SaleView(View):
    def post(self, request, *args, **kwargs):
        sale_form = SaleForm(self.request.POST)
        if sale_form.is_valid():
            sale = sale_form.save()
            sale.save_related()
            messages.success(self.request, Messages.SUCCESSFUL_SALE % {
                'quantity': sale.quantity,
                'measure': sale.product.measure,
                'product': sale.product
            })
        else:
            messages.error(self.request, Messages.UNSUCCESSFUL_SALE)
        return redirect('factory:home')