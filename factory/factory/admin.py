from django.contrib import admin
from django.db.models import F
from factory.admin_forms import PurchaseForm
from factory.models import Measure, Material, Product, JobTitle, Employee, TransactionType, Transaction, Purchase, Sale, \
    Manufacture, ComponentOfProduct


class MaterialInline(admin.TabularInline):
    model = ComponentOfProduct
    fields = ['material', 'quantity']


class ProductModelAdmin(admin.ModelAdmin):
    inlines = [MaterialInline]


class PurchaseModelAdmin(admin.ModelAdmin):
    form = PurchaseForm

    def save_model(self, request, obj, form, change):
        obj.save()
        Transaction.objects.create_purchase_transaction(amount=obj.quantity * obj.material.price, content_object=obj)
        obj.material.quantity = F('quantity') + obj.quantity
        obj.material.save()


admin.site.register(Measure)
admin.site.register(Material)
admin.site.register(Product, ProductModelAdmin)
admin.site.register(JobTitle)
admin.site.register(Employee)
admin.site.register(TransactionType)
admin.site.register(Transaction)
admin.site.register(Purchase, PurchaseModelAdmin)
admin.site.register(Sale)
admin.site.register(Manufacture)