# -*- coding: utf-8 -*-

"""
from django.contrib.admin import site, ModelAdmin
from django.conf import settings

import kinterbasdb

from importer.models import Importer
from client.models import *


class ImporterAdmin(ModelAdmin):
    list_display = ('table','user','datetime_importer','total_new','total_change','message')
    list_filter = ('table','user')
    list_display_links = ('table','user')
    fields = ['table',]
    ordering = ('-datetime_importer','table','user')

    def save_model(self, request, obj, form, change):
        if not change:
            table = obj.table

            if table == 'ICLIENTES':
                fields = 'CDCLIENTE, NMCLIENTE, FANTASIA, CPF, CNPJ, INSCEST, INSCMUN, ENDERECO, COMPLEMENTO, BAIRRO, CIDADE, UF, CEP, DDD, FONE1, FONE2, CELULAR, FAX, EMAIL, CONTATO'
                order = 'ORDER BY CDCLIENTE'
            else:
                fields = '*'
                order = ''

            sql = 'SELECT %s FROM %s %s' % (fields, table, order)

            try:
                # Initial values
                msg_status = ''
                total_new = 0
                total_change = 0

                conn = kinterbasdb.connect(
                    host=settings.FBHOST,
                    database=settings.FBDB,
                    user=settings.FBUSER,
                    password=settings.FBPASS
                )
                cur = conn.cursor()
                cur.execute(sql)
                i = 0
                if table == 'ICLIENTES':
                    for (CDCLIENTE, NMCLIENTE, FANTASIA, CPF, CNPJ, INSCEST, INSCMUN, ENDERECO, COMPLEMENTO, BAIRRO, CIDADE, UF, CEP, DDD, FONE1, FONE2, CELULAR, FAX, EMAIL, CONTATO) in cur:
                        try:
                            c = Client.objects.get(code=CDCLIENTE)
                            total_change += 1
                        except:
                            c = Client()
                            total_new += 1

                            try:
                                if not NMCLIENTE: NMCLIENTE = 'z Sem nome: %s/%s' % (CNPJ,CPF)
                                if not FANTASIA: FANTASIA = NMCLIENTE
                                c.code = CDCLIENTE
                                c.corporate_name = NMCLIENTE.replace('*','')
                                c.fancy_name = FANTASIA.replace('*','')
                                c.cpf = CPF
                                c.cnpj = CNPJ
                                c.ie = INSCEST
                                c.im = INSCMUN
                                c.address = ENDERECO
                                c.complement = COMPLEMENTO
                                c.neighboorhood = BAIRRO
                                c.city = CIDADE
                                c.state = UF
                                c.ddd = DDD
                                c.phone1 = FONE1
                                c.phone2 = FONE2
                                c.fax = FAX
                                c.cell = CELULAR
                                c.email = EMAIL
                                c.contact = CONTATO
                                c.save()

                            except Exception, e:
                                print e.message

                    msg_status = 'Importação de clientes do ILUX'

                if not msg_status == '':
                    obj.user = request.user
                    obj.total_new = total_new
                    obj.total_change = total_change
                    obj.message = msg_status
                    obj.save()


                conn.close()

            except Exception, e:
                print e.message

site.register(Importer, ImporterAdmin)
"""
