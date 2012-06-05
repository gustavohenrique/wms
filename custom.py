# -*- coding: utf-8 -*-
from django.forms.fields import CharField, DecimalField
from django.forms.forms import ValidationError
from django.forms.widgets import Textarea

from decimal import Decimal

class TextField(CharField):
    """
    Create a textarea with max_length=100000
    """

    def __init__(self, max_length=100000, min_length=None, *args, **kwargs):
        self.max_length, self.min_length = max_length, min_length
        self.widget = Textarea
        super(CharField, self).__init__(*args, **kwargs)


class PositiveDecimalField(DecimalField):
    """
    Troca a virgula (,) pelo ponto (.) como separador decimal
    """

    def clean(self, value):
        if not value:
            value = 0
        else:
            try:
                value = Decimal(str(value).replace(',','.').replace('-',''))
            except:
                raise ValidationError('Informe um numero decimal %s' % value)
        return value
