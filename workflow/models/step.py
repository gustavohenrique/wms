# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from process import Process


class Step(models.Model):
    process = models.ForeignKey(Process, verbose_name=u'Processo')
    managers = models.ManyToManyField(User, verbose_name=u'Responsável', related_name='managers')
    participants = models.ManyToManyField(User, blank=True, null=True, verbose_name=u'Quem pode ver', related_name='participants')
    auditor = models.ForeignKey(User, verbose_name=u'Auditor')
    name = models.CharField(max_length=250, verbose_name=u'Nome')
    desc = models.CharField(max_length=250, verbose_name=u'Descrição', blank=True, null=True)
    sequence = models.PositiveSmallIntegerField(verbose_name=u'Ordem')
    #time_limit = models.Field(verbose_name=u'Tempo Limite', max_digits=10, decimal_places=2, blank=True, null=True)
    time_limit = models.PositiveIntegerField(verbose_name=u'Limite (minutos)', default=0, blank=True, null=True)
    can_upload = models.BooleanField(verbose_name=u'Pode anexar documentos?', default=True)
    tasks = models.TextField(max_length=5000, verbose_name=u'Tarefas', blank=True, null=True)

    class Meta:
        db_table = u'wms_step'
        app_label = 'workflow'
        verbose_name = u'passo'
        verbose_name_plural = u'Passos'
        ordering = ['sequence',]

    def __unicode__(self):
        return self.name
