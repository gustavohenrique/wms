# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Process(models.Model):
    #manager = models.ForeignKey(User, verbose_name=u'Gerente')
    name = models.CharField(max_length=250, verbose_name=u'Nome', unique=True)
    desc = models.CharField(max_length=250, verbose_name=u'Descrição', blank=True, null=True)
    users_can_start = models.ManyToManyField(User, verbose_name=u'Quem pode iniciar', related_name='user')

    class Meta:
        app_label = 'workflow'
        db_table = u'wms_process'
        verbose_name = u'processo'
        verbose_name_plural = u'Processos'

    def __unicode__(self):
        return self.name
