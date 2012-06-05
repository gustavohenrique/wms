# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from step import Step
from client.models import Client

class Work(models.Model):
    STATUS_CHOICES = (
        ('A',u'Aberto'),
        ('F',u'Fechado'),
    )
    client = models.ForeignKey(Client, blank=True, null=True, verbose_name='Cliente ILUX')
    previous_step = models.ForeignKey(Step, verbose_name=u'Passo Anterior', related_name='step', blank=True, null=True)
    current_step = models.ForeignKey(Step, verbose_name=u'Passo')
    owner = models.ForeignKey(User, verbose_name=u'Proprietário')
    datetime_add = models.DateTimeField(auto_now_add=True, verbose_name=u'Cadastrado em')
    datetime_change = models.DateTimeField(auto_now=True, verbose_name=u'Atualizado em')
    status = models.CharField(max_length=1, verbose_name=u'Status', choices=STATUS_CHOICES, default='A')
    name = models.CharField(max_length=250, verbose_name=u'Nome', unique=True)
    desc = models.CharField(max_length=250, verbose_name=u'Descrição', blank=True, null=True)
    reject = models.BooleanField(default=False, verbose_name=u'Recusado')
    reason_reject = models.CharField(max_length=250, verbose_name=u'Motivo', blank=True, null=True)

    class Meta:
        app_label = 'workflow'
        db_table = u'wms_work'
        verbose_name = u'trabalho'
        verbose_name_plural = u'Trabalhos'

    def __unicode__(self):
        return self.name


class WorkHistory(models.Model):
    work = models.ForeignKey(Work, verbose_name=u'Trabalho')
    user = models.ForeignKey(User, verbose_name=u'Usuário')
    desc = models.CharField(max_length=250, verbose_name=u'Descrição')
    datetime_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'workflow'
        db_table = u'wms_workhistory'
        verbose_name = u'histórico de trabalho'

    def __unicode__(self):
        return self.desc
