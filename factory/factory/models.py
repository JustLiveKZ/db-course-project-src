from decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.decorators import classonlymethod
from django.utils.translation import ugettext as _
from factory.abstract_models import NamedModelMixin, CountableModelMixin, DateTimeModelMixin, TradeDealModelMixin, MeasurableModelMixin, PricedModelMixin, GenericForeignKeyModelMixin
from factory.constants import TRANSACTION_TYPE_CHOICES, INCOME, OUTCOME
from factory.managers import TransactionManager


class Measure(NamedModelMixin):
    pass


class Material(NamedModelMixin, MeasurableModelMixin, CountableModelMixin, PricedModelMixin):
    pass


class Product(NamedModelMixin, MeasurableModelMixin, CountableModelMixin, PricedModelMixin):
    materials = models.ManyToManyField(Material, related_name='products', through='ComponentOfProduct')


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
    salary = models.DecimalField(max_digits=17, decimal_places=2, validators=[MinValueValidator(0)])
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=40)


class TransactionType(NamedModelMixin):
    type = models.IntegerField(choices=TRANSACTION_TYPE_CHOICES)


class Transaction(DateTimeModelMixin, GenericForeignKeyModelMixin):
    transaction_type = models.ForeignKey(TransactionType)
    amount = models.DecimalField(max_digits=17, decimal_places=2, validators=[MinValueValidator(0)])

    objects = TransactionManager()

    def __unicode__(self):
        return u'%s, %s' % (self.transaction_type, self.amount)

    @classonlymethod
    def get_balance(cls):
        return (cls.objects.filter(transaction_type__type=INCOME).aggregate(Sum('amount')).get('amount__sum') or Decimal(0)) - \
               (cls.objects.filter(transaction_type__type=OUTCOME).aggregate(Sum('amount')).get('amount__sum') or Decimal(0))


class Purchase(TradeDealModelMixin):
    material = models.ForeignKey(Material)

    def __unicode__(self):
        return u'%s, %s %s' % (self.material, self.quantity, self.material.measure)


class Sale(TradeDealModelMixin):
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return u'%s, %s %s' % (self.product, self.quantity, self.product.measure)


class Manufacture(CountableModelMixin, DateTimeModelMixin):
    product = models.ForeignKey(Product)
    employee = models.ForeignKey(Employee)

    def __unicode__(self):
        return u'%s, %s %s' % (self.product, self.quantity, self.product.measure)

    class Meta:
        verbose_name_plural = _('Manufacture')


class Activity(DateTimeModelMixin, GenericForeignKeyModelMixin):
    def __unicode__(self):
        return u'%s' % self.content_object

    class Meta:
        ordering = '-datetime',
        verbose_name_plural = _('Activities')


@receiver(post_save)
def log_activity(sender, instance, **kwargs):
    logging_models = Purchase, Sale, Manufacture, Transaction
    if sender in logging_models:
        Activity.objects.create(content_object=instance)