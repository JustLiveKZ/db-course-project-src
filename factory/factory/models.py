from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils.decorators import classonlymethod

from factory.abstract_models import NamedModelMixin, CountableModelMixin, DateTimeModelMixin, TradeDealModelMixin, MeasurableModelMixin, PricedModelMixin
from factory.constants import TRANSACTION_TYPE_CHOICES, INCOME, OUTCOME


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
        return self.material


class JobTitle(NamedModelMixin):
    pass


class Employee(NamedModelMixin):
    job_title = models.ForeignKey(JobTitle)
    salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=40)


class TransactionType(NamedModelMixin):
    type = models.IntegerField(choices=TRANSACTION_TYPE_CHOICES)


class Transaction(DateTimeModelMixin):
    transaction_type = models.ForeignKey(TransactionType)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return '%s, %s, %s' % (self.amount, self.transaction_type, self.datetime)

    @classonlymethod
    def get_balance(cls):
        return (cls.objects.filter(transaction_type__type=INCOME).aggregate(Sum('amount')).get('amount__sum') or 0.00) - \
               (cls.objects.filter(transaction_type__type=OUTCOME).aggregate(Sum('amount')).get('amount__sum') or 0.00)


class Purchase(TradeDealModelMixin):
    material = models.ForeignKey(Material)

    def __unicode__(self):
        return self.material


class Sale(TradeDealModelMixin):
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return self.product


class Manufacture(CountableModelMixin, DateTimeModelMixin):
    product = models.ForeignKey(Product)
    employee = models.ForeignKey(Employee)

    def __unicode__(self):
        return self.product