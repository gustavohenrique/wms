# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from django.utils import simplejson
from django.forms import ModelChoiceField, Field
from django.forms.fields import CharField, IntegerField
from django.forms.forms import ValidationError
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from workflow.models import *
from wms.utils.extjs import ExtJSONEncoder


class StepAdminForm(ModelForm):
    #time_limit = DecimalField(max_digits=10, decimal_places=2, required=False, label='Tempo Limite')

    class Meta:
        model = Step


class WorkForm(ModelForm):

    class Meta:
        model = Work
        #exclude = ('id','previous_step','current_step','owner','reject','reason_reject','datetime_add','datetime_change','status')
        fields = ['name','desc','client']

    def as_ext(self):
        return mark_safe(simplejson.dumps(self,cls=ExtJSONEncoder))


class AttachForm(ModelForm):
    user = ModelChoiceField(User.objects.all(), required=False)
    work = ModelChoiceField(Work.objects.all(), required=False)

    class Meta:
        model = Attachment
        fields = ['filepath','desc','user','work']
