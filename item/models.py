# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from decimal import Decimal

from workflow.models import Work


class Product(models.Model):
    name = models.CharField(max_length=30, verbose_name='Nome')
    desc = models.CharField(max_length=30, blank=True, null=True, verbose_name='Descrição')
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name='Código')
    partnumber = models.CharField(max_length=10, blank=True, null=True, verbose_name='Partnumber')

    class Meta:
        db_table = 'wms_product'
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class ProductService(models.Model):
    desc = models.CharField(max_length=200, verbose_name='Descrição')

    class Meta:
        db_table = 'wms_productservice'
        verbose_name = 'serviço'
        verbose_name_plural = 'serviços'
        ordering = ['desc']

    def __unicode__(self):
        return self.desc


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, verbose_name='Produto')
    productservice = models.ForeignKey(ProductService, verbose_name='Serviço')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Preço')
    last_update = models.DateTimeField(auto_now=True, verbose_name=u'Atualizado em')

    class Meta:
        db_table = 'wms_productprice'
        verbose_name = 'preço'
        verbose_name_plural = 'preços'
        ordering = ['product']

    def __unicode__(self):
        return u'%s' % self.price


class Item(models.Model):
    product = models.ForeignKey(Product, verbose_name='Produto')
    productprice = models.ForeignKey(ProductPrice, verbose_name='Preço Tabela')
    work = models.ForeignKey(Work, verbose_name='Trabalho')
    user = models.ForeignKey(User, verbose_name='Vendedor')
    amount = models.CharField(max_length=30, verbose_name='Quantidade')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Preço Vendedor')
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Total')
    #type = models.CharField(max_length=100, choices=CHOICES_TYPE, verbose_name='Tipo Serviço')

    class Meta:
        db_table = 'wms_item'
        verbose_name = 'item'
        verbose_name_plural = 'itens'
        ordering = ['product']
        unique_together = (('product','work'),)

    def __unicode__(self):
        return self.product.name

    def save(self):
        self.total = int(self.amount) * Decimal(self.price)
        super(Item, self).save()
