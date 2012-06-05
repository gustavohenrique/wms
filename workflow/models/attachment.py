# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.template.defaultfilters import slugify
#from django.core.files.storage import FileSystemStorage
from django.conf import settings

import re

from work import Work

#fs = FileSystemStorage(location='/tmp/media')

class Attachment(models.Model):
    def _get_file_path_(instance, filename):
        if instance.work:
            #ext = filename[-4:]
            #name_slug = re.sub('[^a-zA-Z0-9]', '-', instance.filename).strip('-').lower()
            #name_slug = re.sub('[-]+', '-', name_slug)
            nome = instance.filepath.__str__().split('/')[-1]
            slug = '%s%s' % (slugify(nome[:-4]), nome[-4:])
            return u'files/%s/%s' % (instance.work.id, slug)

    work = models.ForeignKey(Work, verbose_name=u'Trabalho')
    user = models.ForeignKey(User, verbose_name=u'Dono')
    filepath = models.FileField(upload_to=_get_file_path_, verbose_name=u'Arquivo')
    filename = models.SlugField(max_length=250, verbose_name='slug')
    desc = models.CharField(max_length=250, verbose_name=u'Descrição', blank=True, null=True)
    datetime_change = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        db_table = u'wms_workfiles'
        app_label = 'workflow'
        verbose_name = u'arquivo'
        verbose_name_plural = u'Arquivos'

    def __unicode__(self):
        return u'%s' % self.filepath

    def get_absolute_url(self):
        return '%s%s' % (settings.MEDIA_URL, self.filepath.url)


    #def save(self):
    #    slug = '%s' % slugify(self.filename)
    #    novo_slug = slug
    #    contador = 0
    #    while Attachment.objects.filter(filename=novo_slug).exclude(id=self.id).count() > 0:
    #        contador += 1
    #        novo_slug = '%s-%d'%(slug, contador)
    #    self.filename = novo_slug
    #    super(Attachment, self).save()

def filename_pre_save(signal, instance, sender, **kwargs):
    if instance.filepath:
        nome = instance.filepath.__str__().split('/')[-1]
        slug = '%s%s' % (slugify(nome[:-4]), nome[-4:])
        novo_slug = slug
        print slug
        contador = 0
        while Attachment.objects.filter(filename=novo_slug).exclude(id=instance.id).count() > 0:
            contador += 1
            novo_slug = '%s-%d'%(slug, contador)

        instance.filename = novo_slug
signals.pre_save.connect(filename_pre_save, sender=Attachment)
