from django.contrib import admin
from django.db.models import F

from factory.admin_forms import PurchaseForm, SaleForm, ManufactureForm, TransactionForm
from factory.constants import TransactionTypes
from factory.models import Measure, Material, Product, JobTitle, Employee, TransactionType, Transaction, Purchase, Sale, Manufacture, ComponentOfProduct, Activity


class NotAddableModelAdminMixin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


class NotEditableModelAdminMixin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


class NotDeletableModelAdminMixin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False


class NoBulkActionsModelAdminMixin(admin.ModelAdmin):
    actions = None


class MaterialModelAdmin(admin.ModelAdmin):
    readonly_fields = 'quantity',


class MaterialInline(admin.TabularInline):
    model = ComponentOfProduct
    fields = 'material', 'quantity'
    extra = 0


class ProductModelAdmin(admin.ModelAdmin):
    inlines = [MaterialInline]
    readonly_fields = 'quantity',


class PurchaseModelAdmin(NotDeletableModelAdminMixin, NoBulkActionsModelAdminMixin):
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


class SaleModelAdmin(NotDeletableModelAdminMixin, NoBulkActionsModelAdminMixin):
    form = SaleForm

    def save_model(self, request, obj, form, change):
        obj.save()
        Transaction.objects.create_sale_transaction(amount=obj.quantity * obj.product.price, content_object=obj)
        obj.product.quantity = F('quantity') - obj.quantity
        obj.product.save()


class ManufactureModelAdmin(NotDeletableModelAdminMixin, NoBulkActionsModelAdminMixin):
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


class TransactionModelAdmin(NotDeletableModelAdminMixin, NoBulkActionsModelAdminMixin):
    form = TransactionForm

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return 'transaction_type', 'amount', 'content_type', 'object_id', 'datetime'

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name is 'transaction_type':
            kwargs['queryset'] = TransactionTypes.get_queryset_for_field()
        return super(TransactionModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.save()


class ActivityModelAdmin(NotAddableModelAdminMixin, NotDeletableModelAdminMixin, NoBulkActionsModelAdminMixin):
    readonly_fields = 'content_type', 'object_id', 'datetime'
    list_filter = 'datetime',


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
admin.site.register(Activity, ActivityModelAdmin)