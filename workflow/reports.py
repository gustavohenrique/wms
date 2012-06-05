# -*- coding: utf-8 -*-
from django.conf import settings

import os
IMG_DIR = os.path.join(settings.MEDIA_ROOT, 'images')

#class RelatorioPedido(Report):
#    pass

"""
#from geraldo import Report, ReportBand, ObjectValue, ReportBand, landscape, SystemField, BAND_WIDTH, Label, Image
#from reportlab.lib.units import cm
#from reportlab.lib.pagesizes import landscape, A4
#from reportlab.lib.enums import TA_CENTER, TA_RIGHT

class RelatorioPedido(Report):
    title = 'Pedido'
    print_if_empty = True
    page_size = landscape(A4)

    class band_page_header(ReportBand):
        elements = [
            Image(left=0*cm, top=0*cm, right=0*cm, filename='%s/logo.jpg' % IMG_DIR),
            SystemField(expression='%(now:%d/%m/%Y)s', top=0.1*cm, width=BAND_WIDTH, style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_RIGHT}),
        ]
        borders = {'bottom': True}

    class band_detail(ReportBand):
        height = 0.5*cm
        elements = [
            ObjectValue(attribute_name='dynamicfield.label', left=0.5*cm),
            ObjectValue(attribute_name='value', left=0.5*cm),
        ]



    class band_page_footer(ReportBand):
        height = 0.5*cm
        elements = [
                Label(text='Geraldo Reports', top=0.1*cm),
                ObjectValue(attribute_name='id', width=BAND_WIDTH, display_format='Pedido N. %s', style={'fontName': 'Helvetica-Bold', 'fontSize': 14, 'alignment': TA_RIGHT}),
                ]
        borders = {'top': True}
"""