from django.contrib import admin
from factory.admin_forms import PurchaseForm

from factory.models import Measure, Material, Product, JobTitle, Employee, TransactionType, Transaction, Purchase, Sale, Manufacture, ComponentOfProduct


class MaterialInline(admin.TabularInline):
    model = ComponentOfProduct
    fields = ['material', 'quantity']


class ProductModelAdmin(admin.ModelAdmin):
    inlines = [MaterialInline]


class PurchaseModelAdmin(admin.ModelAdmin):
    form = PurchaseForm


admin.site.register(Measure)
admin.site.register(Material)
admin.site.register(Product, ProductModelAdmin)
admin.site.register(JobTitle)
admin.site.register(Employee)
admin.site.register(TransactionType)
admin.site.register(Transaction)
admin.site.register(Purchase)
admin.site.register(Sale)
admin.site.register(Manufacture)