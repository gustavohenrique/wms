# -*- coding: utf-8 -*-
from django.contrib.admin import site, ModelAdmin, TabularInline

from client.models import *


class ClientAdmin(ModelAdmin):
    list_display = ('code','corporate_name','fancy_name','cnpj','cpf')
site.register(Client, ClientAdmin)
