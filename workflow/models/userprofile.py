# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    plain_password = models.CharField(max_length=10, db_index=True, blank=True, null=True, verbose_name=u'Senha de Alerta')
    user = models.ForeignKey(User, unique=True)

    class Meta:
        db_table = u'wms_userprofile'
        app_label = 'workflow'
