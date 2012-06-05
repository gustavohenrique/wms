# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
#from django.forms.fields import IntegerField

from custom import PositiveDecimalField
from item.models import *
from workflow.models import Work


class ItemForm(ModelForm):
    user = ModelChoiceField(User.objects.all(), required=False)
    work = ModelChoiceField(Work.objects.all(), required=False)
    price = PositiveDecimalField(max_digits=12, decimal_places=2, label='Preço', required=False)

    class Meta:
        model = Item
