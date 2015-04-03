# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('-datetime',),
                'verbose_name_plural': 'Activities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ComponentOfProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.DecimalField(default=Decimal('0'), max_digits=17, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('salary', models.DecimalField(max_digits=17, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=40)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Manufacture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.DecimalField(default=Decimal('0'), max_digits=17, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(to='factory.Employee')),
            ],
            options={
                'verbose_name_plural': 'Manufacture',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(max_digits=17, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('quantity', models.DecimalField(default=Decimal('0'), max_digits=17, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(max_digits=17, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('quantity', models.DecimalField(default=Decimal('0'), max_digits=17, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('materials', models.ManyToManyField(related_name='products', through='factory.ComponentOfProduct', to='factory.Material')),
                ('measure', models.ForeignKey(to='factory.Measure')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.DecimalField(default=Decimal('0'), max_digits=17, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(to='factory.Employee')),
                ('material', models.ForeignKey(to='factory.Material')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.DecimalField(default=Decimal('0'), max_digits=17, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(to='factory.Employee')),
                ('product', models.ForeignKey(to='factory.Product')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('amount', models.DecimalField(max_digits=17, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.IntegerField(choices=[(1, 'Income'), (2, 'Outcome')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.ForeignKey(to='factory.TransactionType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='material',
            name='measure',
            field=models.ForeignKey(to='factory.Measure'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='manufacture',
            name='product',
            field=models.ForeignKey(to='factory.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='job_title',
            field=models.ForeignKey(to='factory.JobTitle'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='componentofproduct',
            name='material',
            field=models.ForeignKey(to='factory.Material'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='componentofproduct',
            name='product',
            field=models.ForeignKey(to='factory.Product'),
            preserve_default=True,
        ),
    ]
