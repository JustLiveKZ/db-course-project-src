from decimal import Decimal
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.db.models import F, Sum
from django.http import HttpResponse

from factory.admin_forms import PurchaseForm, SaleForm, ManufactureForm, TransactionForm
from factory.constants import TransactionTypes
from factory.models import Measure, Material, Product, JobTitle, Employee, TransactionType, Transaction, Purchase, Sale, Manufacture, ComponentOfProduct, Activity, ManufactureExpense


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
    list_display = 'name', 'measure', 'average_price', 'price', 'quantity'

    def get_urls(self):
        urls = super(MaterialModelAdmin, self).get_urls()
        my_urls = [
            url(r'^(.+)/avg_price/$', self.avg_prive, name='material_avg_price'),
        ]
        return my_urls + urls

    def avg_prive(self, request, *args, **kwargs):
        material = Material.objects.get(pk=args[0])
        return HttpResponse(material.average_price)


class MaterialInline(admin.TabularInline):
    def average_price(self, obj):
        return obj.material.average_price

    model = ComponentOfProduct
    fields = 'material', 'quantity', 'average_price'
    readonly_fields = 'average_price',
    extra = 0


class ProductModelAdmin(admin.ModelAdmin):
    inlines = [MaterialInline]
    readonly_fields = 'quantity',
    list_display = 'name', 'measure', 'average_price', 'price', 'quantity'


class EmployeeModelAdmin(admin.ModelAdmin):
    list_display = 'name', 'job_title', 'salary', 'address', 'phone'


class PurchaseModelAdmin(NotDeletableModelAdminMixin, NoBulkActionsModelAdminMixin):
    form = PurchaseForm
    list_display = 'material', 'quantity', 'amount', 'average_price', 'datetime', 'employee'
    list_filter = 'material__name',

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return 'material', 'quantity', 'employee', 'amount'

    def save_model(self, request, obj, form, change):
        if change:
            return
        obj.amount = obj.quantity * obj.material.price
        obj.save()
        Transaction.objects.create_purchase_transaction(amount=obj.amount, content_object=obj)
        obj.material.quantity = F('quantity') + obj.quantity
        obj.material.save()


class SaleModelAdmin(NotDeletableModelAdminMixin, NoBulkActionsModelAdminMixin):
    form = SaleForm
    list_display = 'product', 'quantity', 'datetime', 'employee'

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return 'product', 'quantity', 'datetime', 'employee'

    def save_model(self, request, obj, form, change):
        if change:
            return
        obj.save()
        Transaction.objects.create_sale_transaction(amount=obj.quantity * obj.product.price, content_object=obj)
        obj.product.quantity = F('quantity') - obj.quantity
        obj.product.save()


class ManufactureExpenseInline(admin.TabularInline):
    model = ManufactureExpense
    fields = 'material', 'quantity', 'amount', 'average_price'
    readonly_fields = fields
    extra = 0
    can_delete = False

    def has_add_permission(self, request):
        return False


class ManufactureModelAdmin(NotDeletableModelAdminMixin, NoBulkActionsModelAdminMixin):
    form = ManufactureForm
    list_display = 'product', 'quantity', 'amount', 'average_price', 'datetime', 'employee'
    list_filter = 'product__name',
    inlines = [ManufactureExpenseInline]

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return 'product', 'quantity', 'employee', 'datetime'

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super(ManufactureModelAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [ManufactureExpenseInline]
        return super(ManufactureModelAdmin, self).change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        """
        :type obj: Manufacture
        """
        if change:
            return
        obj.save()
        for component in obj.product.componentofproduct_set.all():
            component.material.quantity = F('quantity') - obj.quantity * component.quantity
            component.material.save()
            manufacture_expense = ManufactureExpense()
            manufacture_expense.material = component.material
            manufacture_expense.quantity = component.quantity * obj.quantity
            manufacture_expense.amount = manufacture_expense.quantity * component.material.average_price
            obj.expenses.add(manufacture_expense)
        obj.amount = obj.expenses.aggregate(Sum('amount')).get('amount__sum', Decimal(0))
        obj.save()
        obj.product.quantity = F('quantity') + obj.quantity
        obj.product.save()


class TransactionModelAdmin(NotDeletableModelAdminMixin, NoBulkActionsModelAdminMixin):
    form = TransactionForm
    list_display = 'transaction_type', 'content_object', 'amount', 'datetime'

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ()
        return 'transaction_type', 'amount', 'content_type', 'object_id', 'datetime'

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name is 'transaction_type':
            kwargs['queryset'] = TransactionTypes.get_queryset_for_field()
        return super(TransactionModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['balance'] = Transaction.get_balance()
        return super(TransactionModelAdmin, self).changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if change:
            return
        obj.save()


class ActivityModelAdmin(NotAddableModelAdminMixin, NotDeletableModelAdminMixin, NoBulkActionsModelAdminMixin):
    readonly_fields = 'content_type', 'object_id', 'datetime'
    list_filter = 'datetime',
    list_display = 'datetime', 'content_type', 'content_object'
    list_display_links = None


admin.site.register(Measure)
admin.site.register(Material, MaterialModelAdmin)
admin.site.register(Product, ProductModelAdmin)
admin.site.register(JobTitle)
admin.site.register(Employee, EmployeeModelAdmin)
admin.site.register(TransactionType)
admin.site.register(Transaction, TransactionModelAdmin)
admin.site.register(Purchase, PurchaseModelAdmin)
admin.site.register(Sale, SaleModelAdmin)
admin.site.register(Manufacture, ManufactureModelAdmin)
admin.site.register(Activity, ActivityModelAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)