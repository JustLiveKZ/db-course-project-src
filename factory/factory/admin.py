from django.contrib import admin
from django.db.models import F

from factory.admin_forms import PurchaseForm, SaleForm, ManufactureForm
from factory.models import Measure, Material, Product, JobTitle, Employee, TransactionType, Transaction, Purchase, Sale, Manufacture, \
    ComponentOfProduct


class MaterialModelAdmin(admin.ModelAdmin):
    readonly_fields = 'quantity',


class MaterialInline(admin.TabularInline):
    model = ComponentOfProduct
    fields = 'material', 'quantity'
    extra = 0


class ProductModelAdmin(admin.ModelAdmin):
    inlines = [MaterialInline]
    readonly_fields = 'quantity',


class PurchaseModelAdmin(admin.ModelAdmin):
    form = PurchaseForm

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return 'material', 'quantity', 'employee'

    def save_model(self, request, obj, form, change):
        obj.save()
        Transaction.objects.create_purchase_transaction(amount=obj.quantity * obj.material.price, content_object=obj)
        obj.material.quantity = F('quantity') + obj.quantity
        obj.material.save()


class SaleModelAdmin(admin.ModelAdmin):
    form = SaleForm

    def save_model(self, request, obj, form, change):
        obj.save()
        Transaction.objects.create_sale_transaction(amount=obj.quantity * obj.product.price, content_object=obj)
        obj.product.quantity = F('quantity') - obj.quantity
        obj.product.save()


class ManufactureModelAdmin(admin.ModelAdmin):
    form = ManufactureForm

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return 'product', 'quantity', 'employee', 'datetime'

    def save_model(self, request, obj, form, change):
        obj.save()
        for component in obj.product.componentofproduct_set.all():
            component.material.quantity = F('quantity') - obj.quantity * component.quantity
            component.material.save()
        obj.product.quantity = F('quantity') + obj.quantity
        obj.product.save()


class TransactionModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return 'transaction_type', 'amount', 'content_type', 'object_id', 'datetime'


admin.site.register(Measure)
admin.site.register(Material, MaterialModelAdmin)
admin.site.register(Product, ProductModelAdmin)
admin.site.register(JobTitle)
admin.site.register(Employee)
admin.site.register(TransactionType)
admin.site.register(Transaction, TransactionModelAdmin)
admin.site.register(Purchase, PurchaseModelAdmin)
admin.site.register(Sale, SaleModelAdmin)
admin.site.register(Manufacture, ManufactureModelAdmin)