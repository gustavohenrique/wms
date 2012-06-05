# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User


class Importer(models.Model):
    TABLE_CHOICES = (
        ('IPRODUTOS', 'Produtos'),
        ('ICLIENTES', 'Clientes'),
    )
    user = models.ForeignKey(User)
    table = models.CharField(max_length=50, choices=TABLE_CHOICES, verbose_name=u'Tabela')
    datetime_importer = models.DateTimeField(auto_now_add=True, verbose_name=u'Data Importação')
    total_new = models.PositiveIntegerField(blank=True, null=True, verbose_name='Novos registros')
    total_change = models.PositiveIntegerField(blank=True, null=True, verbose_name='Registros atualizados')
    message = models.CharField(max_length=250, blank=True, null=True, verbose_name=u'Resposta')

    class Meta:
        db_table = 'wms_importer'
        verbose_name = u'importação'
        verbose_name_plural = u'importações'

    def __unicode__(self):
        return self.table
