from decimal import Decimal
from abc import ABCMeta, abstractmethod
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models


class NamedModelMixin(models.Model):
    name = models.CharField(max_length=100, )

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class MeasurableModelMixin(models.Model):
    measure = models.ForeignKey('factory.Measure')

    class Meta:
        abstract = True


class PricedModelMixin(models.Model):
    price = models.DecimalField(max_digits=17, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        abstract = True


class CountableModelMixin(models.Model):
    quantity = models.DecimalField(max_digits=17, decimal_places=2, validators=[MinValueValidator(0)], default=Decimal(0))

    class Meta:
        abstract = True


class DateTimeModelMixin(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TradeDealModelMixin(CountableModelMixin, DateTimeModelMixin):
    employee = models.ForeignKey('factory.Employee')

    class Meta:
        abstract = True


class GenericForeignKeyModelMixin(models.Model):
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey()

    class Meta:
        abstract = True


class LogViewInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def as_tr(self):
        pass