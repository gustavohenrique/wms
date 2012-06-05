# -*- coding: utf-8 -*-
from django.db import models


class Client(models.Model):
    code = models.PositiveIntegerField(verbose_name=u'Código Ilux')
    corporate_name = models.CharField(max_length=50, verbose_name='Razão Social')
    fancy_name = models.CharField(max_length=30, verbose_name='Nome Fantasia')
    cpf = models.CharField(max_length=14, blank=True, null=True, verbose_name='CPF')
    cnpj = models.CharField(max_length=19, blank=True, null=True, verbose_name='CNPJ')
    ie = models.CharField(max_length=20, blank=True, null=True, verbose_name='IE/RG')
    im = models.CharField(max_length=20, blank=True, null=True, verbose_name='Insc. Municipal')
    address = models.CharField(max_length=50, blank=True, null=True, verbose_name='Endereço')
    complement = models.CharField(max_length=30, blank=True, null=True, verbose_name='Complemento')
    neighboorhood = models.CharField(max_length=30, blank=True, null=True, verbose_name='Bairro')
    city = models.CharField(max_length=40, blank=True, null=True, verbose_name='Cidade')
    state = models.CharField(max_length=2, blank=True, null=True, verbose_name='UF')
    cep = models.CharField(max_length=8, blank=True, null=True, verbose_name='CEP')
    ddd = models.CharField(max_length=10, blank=True, null=True, verbose_name='DDD')
    phone1 = models.CharField(max_length=15, blank=True, null=True, verbose_name='Fone1')
    phone2 = models.CharField(max_length=15, blank=True, null=True, verbose_name='Fone2')
    fax = models.CharField(max_length=15, blank=True, null=True, verbose_name='Fax')
    cell = models.CharField(max_length=15, blank=True, null=True, verbose_name='Celular')
    email = models.CharField(max_length=52, blank=True, null=True, verbose_name='E-mail')
    contact = models.CharField(max_length=20, blank=True, null=True, verbose_name='Contato')

    class Meta:
        db_table = 'wms_client'
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
        ordering = ['fancy_name']

    def __unicode__(self):
        return self.fancy_name

