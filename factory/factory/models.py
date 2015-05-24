from __future__ import division

from decimal import Decimal, InvalidOperation, getcontext

from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.decorators import classonlymethod
from django.utils.translation import ugettext as _
from factory.abstract_models import NamedModelMixin, CountableModelMixin, DateTimeModelMixin, TradeDealModelMixin, MeasurableModelMixin, PricedModelMixin, GenericForeignKeyModelMixin
from factory.constants import TRANSACTION_TYPE_CHOICES, INCOME, OUTCOME, TWO_DECIMAL_PLACES
from factory.managers import TransactionManager


class Measure(NamedModelMixin):
    pass


class Material(NamedModelMixin, MeasurableModelMixin, CountableModelMixin, PricedModelMixin):
    @property
    def average_price(self):
        try:
            average_price = (Purchase.objects.filter(material=self).aggregate(Sum('amount')).get('amount__sum', Decimal(0))) / \
                            (Purchase.objects.filter(material=self).aggregate(Sum('quantity')).get('quantity__sum', Decimal(0)))
            return average_price.quantize(TWO_DECIMAL_PLACES)
        except InvalidOperation:
            return None


class Product(NamedModelMixin, MeasurableModelMixin, CountableModelMixin, PricedModelMixin):
    materials = models.ManyToManyField(Material, related_name='products', through='ComponentOfProduct')

    @property
    def average_price(self):
        try:
            average_price = (Manufacture.objects.filter(product=self).aggregate(Sum('amount')).get('amount__sum', Decimal(0))) / \
                            (Manufacture.objects.filter(product=self).aggregate(Sum('quantity')).get('quantity__sum', Decimal(0)))
            return average_price.quantize(TWO_DECIMAL_PLACES)
        except InvalidOperation:
            return None


class ComponentOfProduct(CountableModelMixin):
    material = models.ForeignKey(Material)
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return u'%s' % self.material

    class Meta:
        unique_together = 'material', 'product'


class JobTitle(NamedModelMixin):
    pass


class Employee(NamedModelMixin):
    job_title = models.ForeignKey(JobTitle)
    salary = models.DecimalField(max_digits=17, decimal_places=2, default=Decimal(0), validators=[MinValueValidator(0)])
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=40)


class TransactionType(NamedModelMixin):
    type = models.IntegerField(choices=TRANSACTION_TYPE_CHOICES)


class Transaction(DateTimeModelMixin, GenericForeignKeyModelMixin):
    transaction_type = models.ForeignKey(TransactionType)
    amount = models.DecimalField(max_digits=17, decimal_places=2, default=Decimal(0), validators=[MinValueValidator(0)])

    objects = TransactionManager()

    def __unicode__(self):
        return u'%s, %s' % (self.transaction_type, self.amount)

    @classonlymethod
    def get_balance(cls):
        return (cls.objects.filter(transaction_type__type=INCOME).aggregate(Sum('amount')).get('amount__sum', Decimal(0))) - \
               (cls.objects.filter(transaction_type__type=OUTCOME).aggregate(Sum('amount')).get('amount__sum', Decimal(0)))


class Purchase(TradeDealModelMixin):
    material = models.ForeignKey(Material)
    amount = models.DecimalField(max_digits=17, decimal_places=2, default=Decimal(0), validators=[MinValueValidator(0)])

    @property
    def average_price(self):
        try:
            return self.amount / self.quantity
        except InvalidOperation:
            return None

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.amount = self.quantity * self.material.price
        return super(Purchase, self).save(force_insert, force_update, using, update_fields)

    def save_related(self):
        Transaction.objects.create_purchase_transaction(amount=self.amount, content_object=self)
        self.material.quantity = F('quantity') + self.quantity
        self.material.save()

    def __unicode__(self):
        return u'%s, %s %s' % (self.material, self.quantity, self.material.measure)


class Sale(TradeDealModelMixin):
    product = models.ForeignKey(Product)

    def save_related(self):
        Transaction.objects.create_sale_transaction(amount=self.quantity * self.product.price, content_object=self)
        self.product.quantity = F('quantity') - self.quantity
        self.product.save()

    def __unicode__(self):
        return u'%s, %s %s' % (self.product, self.quantity, self.product.measure)


class Manufacture(TradeDealModelMixin):
    product = models.ForeignKey(Product)
    amount = models.DecimalField(max_digits=17, decimal_places=2, default=Decimal(0), validators=[MinValueValidator(0)])

    @property
    def average_price(self):
        try:
            return self.amount / self.quantity
        except InvalidOperation:
            return None

    def save_related(self):
        for component in self.product.componentofproduct_set.all():
            component.material.quantity = F('quantity') - self.quantity * component.quantity
            component.material.save()
            manufacture_expense = ManufactureExpense()
            manufacture_expense.material = component.material
            manufacture_expense.quantity = component.quantity * self.quantity
            manufacture_expense.amount = manufacture_expense.quantity * component.material.average_price
            self.expenses.add(manufacture_expense)
        self.amount = self.expenses.aggregate(Sum('amount')).get('amount__sum', Decimal(0))
        self.save()
        self.product.quantity = F('quantity') + self.quantity
        self.product.save()

    def __unicode__(self):
        return u'%s, %s %s' % (self.product, self.quantity, self.product.measure)

    class Meta:
        verbose_name_plural = _('Manufacture')


class ManufactureExpense(CountableModelMixin):
    manufacture = models.ForeignKey(Manufacture, related_name='expenses')
    material = models.ForeignKey(Material)
    amount = models.DecimalField(max_digits=17, decimal_places=2, default=Decimal(0), validators=[MinValueValidator(0)])

    @property
    def average_price(self):
        try:
            return ((self.amount or Decimal(0)) / (self.quantity or Decimal(0))).quantize(TWO_DECIMAL_PLACES)
        except InvalidOperation:
            return None

    def __unicode__(self):
        return u'%s' % self.material


class Activity(DateTimeModelMixin, GenericForeignKeyModelMixin):
    def __unicode__(self):
        return u'%s' % self.content_object

    class Meta:
        ordering = '-datetime',
        verbose_name_plural = _('Activities')


@receiver(post_save)
def log_activity(sender, instance, created, **kwargs):
    logging_models = Purchase, Sale, Manufacture, Transaction
    if created and sender in logging_models:
        Activity.objects.create(content_object=instance)