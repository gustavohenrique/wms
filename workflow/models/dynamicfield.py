# -*- coding: utf-8 -*-
from django.db import models
from django.template.defaultfilters import slugify

from step import Step
from process import Process
from work import Work

class DynamicField(models.Model):
    TYPE_CHOICES = (
        ('CharField',u'Texto simples (max 255)'),
        ('TextField',u'Texto Extenso'),
        ('IntegerField',u'Número Inteiro'),
        ('DateField',u'Data'),
        ('EmailField',u'E-mail'),
        ('DecimalField',u'Número Decimal'),
        ('BooleanField',u'Sim ou Não'),
    )
    name = models.SlugField(max_length=250, verbose_name=u'Campo', db_index=True, unique=True)
    fieldtype = models.CharField(max_length=250, verbose_name=u'Tipo', choices=TYPE_CHOICES)
    label = models.CharField(max_length=50, verbose_name=u'Nome')
    initial = models.CharField(max_length=250, verbose_name=u'Valor Inicial', blank=True, null=True)
    required = models.BooleanField(default=True, verbose_name=u'Obrigatório')
    max_length = models.PositiveSmallIntegerField(max_length=3, verbose_name=u'Máximo caracteres', blank=True, null=True)
    sequence = models.PositiveSmallIntegerField(default=0, verbose_name=u'Ordem')

    class Meta:
        abstract = True


class DynamicFieldProcess(DynamicField):
    process = models.ForeignKey(Process, verbose_name=u'Processo')

    class Meta:
        app_label = 'workflow'
        db_table = u'wms_dynamicfieldprocess'
        verbose_name = u'campo'
        verbose_name_plural = u'campos'

    def __unicode__(self):
        return self.name

    def save(self):
        if self.label:
            slug = slugify(self.label).replace('-','')
            slug2 = slug
            contador = 0

            while DynamicFieldProcess.objects.filter(name=slug2).exclude(id=self.id).count() > 0:
                contador += 1
                slug2 = '%s-%d'%(slug, contador)

            self.name = slug2
        super(DynamicFieldProcess, self).save()


class DynamicFieldStep(DynamicField):
    step = models.ForeignKey(Step, verbose_name=u'Passo')

    class Meta:
        app_label = 'workflow'
        db_table = u'wms_dynamicfieldstep'
        verbose_name = u'campo'
        verbose_name_plural = u'campos'

    def __unicode__(self):
        return self.name

    def save(self):
        if self.label:
            slug = slugify(self.label)
            slug2 = slug
            contador = 0

            while DynamicFieldStep.objects.filter(name=slug2).exclude(id=self.id).count() > 0:
                contador += 1
                slug2 = '%s-%d'%(slug, contador)

            self.name = slug2
        super(DynamicFieldStep, self).save()


class WorkFieldValue(models.Model):
    work = models.ForeignKey(Work, verbose_name=u'Trabalho')
    dynamicfield = models.ForeignKey(DynamicFieldStep, verbose_name=u'Campo')
    value = models.TextField(max_length=100000, verbose_name=u'Valor')

    class Meta:
        app_label = 'workflow'
        db_table = u'wms_workfieldvalue'
        verbose_name = u'dado de trabalho'
        verbose_name_plural = u'dados de trabalho'

    def __unicode__(self):
        return self.value


class ProcessFieldValue(models.Model):
    process = models.ForeignKey(Process, verbose_name=u'Processo')
    work = models.ForeignKey(Work, verbose_name=u'Trabalho')
    dynamicfield = models.ForeignKey(DynamicFieldProcess, verbose_name=u'Campo')
    value = models.TextField(max_length=100000, verbose_name=u'Valor')

    class Meta:
        app_label = 'workflow'
        db_table = u'wms_processfieldvalue'
        verbose_name = u'dado de processo'
        verbose_name_plural = u'dados de processo'

    def __unicode__(self):
        return self.value