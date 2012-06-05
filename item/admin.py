# -*- coding: utf-8 -*-
from django.contrib.admin import site, ModelAdmin

from item.models import *

class ProductAdmin(ModelAdmin):
    list_display = ('name','code','partnumber')
site.register(Product, ProductAdmin)

class ProductPriceAdmin(ModelAdmin):
    list_display = ('product','productservice','price','last_update')
site.register(ProductPrice, ProductPriceAdmin)

class ItemAdmin(ModelAdmin):
    list_display = ('product','amount','price','productprice','work','user')
    list_filter = ('work',)
site.register(Item, ItemAdmin)

site.register(ProductService)