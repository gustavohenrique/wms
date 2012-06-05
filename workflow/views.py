# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse as R
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils import simplejson
from django.forms import forms, fields
from django.forms.models import ModelChoiceField
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.forms.widgets import DateTimeInput

from wms.utils.extjs import ExtJSONEncoder
from django.utils.safestring import mark_safe
import os, sys, datetime

from workflow.models import *
from workflow.forms import *
from workflow.decorators import *
from workflow.reports import *
from client.models import *
from item.models import *
from item.forms import *
from custom import TextField
from report import write_pdf

#from geraldo.generators import PDFGenerator


@login_required
def index(request):
    """
    Show the main page
    """

    ps = ProductService.objects.all()
    if ps.count() > 0:
        product_service = []
        for item in ps:
            try:
                item.productprice_set.select_related().get(price__gt=0)
                product_service.append([int(item.id), item.desc.encode('ascii','xmlcharrefreplace')])
            except:
                pass

    else:
        product_service = [[0, 'Nenhum servico cadastrado']]

    return direct_to_template(request, 'index.html', extra_context={'product_service': product_service})


@login_required
def menu(request):
    """
    Return the values for a treemenu
    """

    # Admin tem acesso a todos os steps de todos os processos
    #if request.user.is_superuser:
    #    s = Step.objects.all().order_by('process','sequence')
    #else:
        #s = Step.objects.filter(managers=request.user).order_by('process','sequence')
    s = Step.objects.all().order_by('process','sequence')
    process_added = []
    menu = []
    temp = {}
    #import ipdb
    #ipdb.set_trace()
    for step in s:
        # Verifica se o usuario pode iniciar um trabalho
        #try:
        #    step.process.users_can_start.get(username=request.user)
        can_start_process = True
        #except:
        #    can_start_process = False

        #try:
        #    #step.process.users_can_participate.get(username=request.user)
        #    step.participants.get(username=request.user)
        can_participate_step = True
        #except:
        #    can_participate_step = False
        # Obtem o toal de trabalhos abertos e exibe ao lado do passo
        total_open = Work.objects.filter(current_step=step, status='A').count()
        if total_open > 0:
            total_open_str = '<span style="color:red;">(%s)</span>' % total_open
        else:
            total_open_str = ''

        step_title_menu = '<span style="color:black">%s.</span> %s %s' % (step.sequence, step.name, total_open_str)
        # Se o usuario logado for o responsavel pelo passo a cor do titulo é azul
        try:
            step.managers.get(username=request.user)
            step_title_menu = '<span style="color:blue">%s</span>' % step_title_menu
            can_manager_step = True
        except:
            # Se nao for o responsavel mas participar do processo, a cor do titulo é cinza
            can_manager_step = False
            if can_participate_step:
                step_title_menu = '<span style="color:gray">%s</span>' % step_title_menu

        if can_manager_step or can_participate_step:

            # Se o processo nao estiver na lista...
            if not step.process.name in process_added:
                # Adiciona o processo a lista
                process_added.append(step.process.name)
                # Cria a arvore cujo nome eh o mesmo do processo e insere o primeiro passo
                children = []
                if can_start_process == True:
                    # Botao Novo
                    children.append({'pk': 0, 'process_id': step.process.id, 'process_name': step.process.name, 'text': 'Novo', 'leaf': True, 'iconCls': 'add-icon'})
                children.append({
                    'pk': step.id,
                    'process_id': step.process.id,
                    'process_name': step.process.name,
                    'step_name': step.name,
                    'text': step_title_menu,
                    'leaf': True,
                    'manager': can_manager_step,
                    'participant': can_participate_step
                })

                temp = {
                    step.process.name: {
                        'text': step.process.name,
                        'id': step.process.id,
                        'cls': 'file',
                        'expanded': True,
                        'children': children,
                    }
                }
                # Adiciona a lista o menu
                menu.append(temp)
            else:
                # Se o processo ja esta na lista...
                # Varre a lista menu
                for cont in range(len(menu)):
                    # Verifica se o nome do processo eh a chave do menu
                    if menu[cont].has_key(step.process.name):
                        # Se for, adiciona um nó ao menu
                        menu[cont][step.process.name]['children'].append({
                            'pk': step.id,
                            'process_id': step.process.id,
                            'process_name': step.process.name,
                            'step_name': step.name,
                            'text': step_title_menu,
                            'leaf': True,
                            'manager': can_manager_step,
                            'participant': can_participate_step,
                        })

    m = []
    for item in menu:
        m.append(item.values()[0])

    json = simplejson.dumps(m)
    return R(json, mimetype='application/json')


@login_required
def get_step_tasks(request):
    """
    Return the tasks of step
    """

    if request.method == 'POST':
        try:
            step_id = int(request.POST.get('step'))
            s = Step.objects.get(pk=step_id)
            tasks = {'tasks': s.tasks}
        except:
            tasks = {'tasks': ''}

        json = simplejson.dumps(tasks)
        return R(json,mimetype='application/json')


class ProcessView(object):
    @login_required
    def work(self, request):
        """
        Return the works from process
        """

        if request.is_ajax(): # == 'POST':
            try:
                process_id = int(request.GET.get('process'))
                step_id = int(request.GET.get('step'))
                w = Work.objects.filter(current_step__process=process_id).exclude(current_step=step_id, status='A').order_by('status','datetime_change')
                if w.count() > 0:
                    rows = []
                    for item in w:
                        d = {
                            'id': item.pk,
                            'name': unicode(item.name),
                            'current_step': unicode(item.current_step),
                            'desc': item.desc,
                            'owner': unicode(item.owner),
                            'datetime_add': item.datetime_add.strftime('%d/%m/%Y %H:%M'),
                            'datetime_change': item.datetime_change.strftime('%d/%m/%Y %H:%M'),
                            'reject': [u'Não', u'Sim'] [item.reject],
                            'reason_reject': item.reason_reject,
                            'status': [u'Fechado', u'Aberto'] [item.status == 'A'],
                            'can_upload': item.current_step.can_upload,
                        }
                        rows.append(d)
                    r = {'total': len(w.values()), 'rows': rows}
                else:
                    r = {'total': 0, 'rows': [{'id':0 , 'name':'Nenhum resultado'}]}
            except:
                r = {'total': 0, 'rows': [{'id':0 , 'name':'nada'}]}

            json = simplejson.dumps(r)
            return R(json,mimetype='application/json')
        else:
            return R('not ajax')


class WorkView(object):
    def __insert_work_history(self, w, u, d):
        """
        Create a history about work
        """

        try:
            h = WorkHistory.objects.create(work=w, user=u, desc=d)
            h.save()
            return True
        except:
            return False


    def __get_dynamicworkform(self, step_id, work_id=None):
        d = DynamicFieldStep.objects.filter(step=step_id).order_by('sequence')
        if d.count() == 0:
            return False
        dynfields = {}
        for f in d:
            max_length = [250, f.max_length][f.max_length > 0]
            required = [False, True][f.required]

            # Try get value, if the field already exist. For exampĺe, a reject work
            try:
                initial = u'' % WorkFieldValue.objects.get(dynamicfield=f, work=work_id).value
            except:
                initial = None


            if f.fieldtype == 'CharField':
                formfield = fields.CharField(max_length=max_length, required=required, label=f.label, initial=initial)

            if f.fieldtype == 'TextField':
                formfield = TextField(required=required, label=f.label, initial=initial)

            if f.fieldtype == 'EmailField':
                formfield = fields.EmailField(max_length=max_length, required=required, label=f.label, initial=initial)

            if f.fieldtype == 'DateField':
                formfield = fields.DateField(('%d/%m/%Y',), widget=DateTimeInput(format='%d/%m/%Y', attrs={'class':'brdatefield', 'maxlength':'10'}), required=required, label=f.label, initial=initial)

            if f.fieldtype == 'IntegerField':
                formfield = fields.IntegerField(required=required, label=f.label, min_value=0, initial=initial)

            if f.fieldtype == 'DecimalField':
                formfield = fields.DecimalField(max_digits=10, decimal_places=2, required=required, label=f.label, initial=initial)

            if f.fieldtype == 'BooleanField':
                formfield = fields.BooleanField(required=False, label=f.label, initial='true')

            if f.fieldtype == 'FileField':
                formfield = fields.FileField(required=required, label=f.label, initial=initial)


            dynfields[f.name] = formfield


            process = f.step.process
            sequence = f.step.sequence

        next_steps = Step.objects.filter(process=process,sequence__gt=sequence).order_by('sequence')
        if next_steps.count() > 0:
            for n in next_steps:
                if n.sequence == sequence + 1: selected = n.pk
            if not selected:
                selected = n.pk
            dynfields['step'] = ModelChoiceField(queryset=next_steps, label=u'Próximo Passo', empty_label=None, initial=selected)

        form = type('', (forms.Form,), dynfields)
        def as_ext(self):
            return mark_safe(simplejson.dumps(self,cls=ExtJSONEncoder))
        form.as_ext = as_ext
        return form


    def __get_dynamicprocessform(self, process_id):
        d = DynamicFieldProcess.objects.filter(process=process_id).order_by('sequence')
        if d.count() == 0:
            return False
        dynfields = {}
        for f in d:
            max_length = [250, f.max_length][f.max_length > 0]
            required = [False, True][f.required]
            initial = None

            if f.fieldtype == 'CharField':
                formfield = fields.CharField(max_length=max_length, required=required, label=f.label, initial=initial)

            if f.fieldtype == 'TextField':
                formfield = TextField(required=required, label=f.label, initial=initial)

            if f.fieldtype == 'EmailField':
                formfield = fields.EmailField(max_length=max_length, required=required, label=f.label, initial=initial)

            if f.fieldtype == 'DateField':
                formfield = fields.DateField(('%d/%m/%Y',), widget=DateTimeInput(format='%d/%m/%Y', attrs={'class':'brdatefield', 'maxlength':'10'}), required=required, label=f.label, initial=initial)

            if f.fieldtype == 'IntegerField':
                formfield = fields.IntegerField(required=required, label=f.label, min_value=0, initial=initial)

            if f.fieldtype == 'DecimalField':
                formfield = fields.DecimalField(max_digits=10, decimal_places=2, required=required, label=f.label, initial=initial)

            if f.fieldtype == 'BooleanField':
                formfield = fields.BooleanField(required=False, label=f.label, initial='true')

            if f.fieldtype == 'FileField':
                formfield = fields.FileField(required=required, label=f.label, initial=initial)

            dynfields[f.name] = formfield

        form = type('', (forms.Form,), dynfields)
        def as_ext(self):
            return mark_safe(simplejson.dumps(self,cls=ExtJSONEncoder))
        form.as_ext = as_ext
        return form


    @login_required
    def form_accept(self, request):
        """
        Make the form for accept work
        """

        try:
            work_id = int(request.GET.get('work'))
            w = Work.objects.get(pk=work_id, status='A')
            form = self.__get_dynamicworkform(w.current_step.pk, w.pk)
            if form:
                f = form()
                json = f.as_ext()
            else:
                json = '{"success": true, "status": "error", "msg": "Not form"}'
        except Exception, e:
            json = '{"success": true, "status": "error", "msg": "%s"}' % e.message

        return R(json,mimetype='application/json')


    @login_required
    def get(self, request):
        """
        Return the step's works for a grid
        """

        if request.is_ajax(): # == 'POST':
            try:
                step_id = int(request.GET.get('step'))
                w = Work.objects.filter(current_step=step_id, status='A').order_by('status','datetime_change')
                if w.count() > 0:

                    rows = []
                    for item in w:
                        datetime_limit = item.datetime_change + datetime.timedelta(minutes=item.current_step.time_limit)
                        d = {
                            'id': item.pk,
                            'name': unicode(item.name),
                            'desc': item.desc,
                            'owner': unicode(item.owner),
                            'datetime_add': item.datetime_add.strftime('%d/%m/%Y %H:%M'),
                            'datetime_change': item.datetime_change.strftime('%d/%m/%Y %H:%M'),
                            'datetime_limit': datetime_limit.strftime('%d/%m/%Y %H:%M'),
                            'reject': [u'Não', u'Sim'] [item.reject],
                            'reason_reject': item.reason_reject,
                            'status': [u'Fechado', u'Aberto'] [item.status == 'A'],
                            'can_upload': item.current_step.can_upload,
                        }
                        rows.append(d)
                    r = {'total': len(w.values()), 'rows': rows}
                else:
                    r = {'total': 0, 'rows': [{'id':0 , 'name':'Nenhum resultado'}]}
            except:
                r = {'total': 0, 'rows': [{'id':0 , 'name':'nada'}]}

            json = simplejson.dumps(r)
            return R(json,mimetype='application/json')
        else:
            return R('not ajax')


    @login_required
    def new(self, request):
        """
        Make the form for new work
        """

        try:
            process_id = request.GET.get('process')
            form = self.__get_dynamicprocessform(process_id)
            if form:
                f1 = WorkForm()
                f2 = form()
                json = '%s%s' % (f1.as_ext(), f2.as_ext())
                json = json.replace('][',',')
            else:
                json = '{"success": true, "status": "error", "msg": "Not form"}'
        except Exception, e:
            json = '{"success": true, "status": "error", "msg": "%s"}' % e.message

        return R(json,mimetype='application/json')


    @login_required
    def add(self, request):
        """
        Adiciona um novo trabalho
        """

        msg = ''
        status = 'error'
        if request.is_ajax():
            P = request.POST
            try:
                process_id = int(request.GET.get('process'))
            except Exception, e:
                msg = e.message

            f1 = WorkForm(P)
            f2 = self.__get_dynamicprocessform(process_id)(P)
            form = None
            # check f1 is valid so...
            if f1.is_valid():
                # check f2 is valid so...
                if f2.is_valid():
                    # add work in the first step
                    try:
                        s = Step.objects.get(process=process_id, sequence=1)
                        # verify if user has permission to start a new work in the process
                        try:
                            s.process.users_can_start.get(username=request.user)
                            w = Work()
                            w.current_step = s
                            w.name = P.get('name')
                            w.desc = P.get('desc')
                            w.owner = request.user
                            try:
                                w.client = Client.objects.get(id=P.get('client'))
                            except:
                                pass
                            try:
                                w.save()
                                status = 'ok'

                                # save the values of the dynamic fields
                                for k in P.keys():
                                    try:
                                        dynfield = DynamicFieldProcess.objects.get(name=k)
                                        value = P.get(k)

                                        if dynfield.fieldtype == 'BooleanField':
                                            value =  value == 'true' and 'Sim' or 'Nao'
                                        elif dynfield.fieldtype == 'DecimalField':
                                            value = value == '' and 0 or value.replace(',','.')

                                        try:
                                            p = ProcessFieldValue.objects.create(
                                                process=w.current_step.process,
                                                work = w,
                                                dynamicfield=dynfield,
                                                value=value
                                            )
                                            p.save()
                                            status = 'ok'
                                            msg = 'Sucesso! Trabalho encaminhado ao próximo passo'
                                        except Exception, e:
                                            msg = 'ProcessFieldValue error: %s' % e.message
                                    except Exception, e:
                                        # fields in post don't match
                                        msg = 'Error: %s' % e.message

                                self.__insert_work_history(w, request.user, u'Novo trabalho criado.')
                            except Exception, e:
                                msg = 'Save error: %s' % e.message

                        except Exception, e:
                                msg = 'No permission, %s' % e.message


                    except Exception, e:
                        msg = 'Error Process ID %s: %s' % (process_id, e.message)
                else:
                    form = f2
            else:
                form = f1

            if form:
                for field in form:
                    if field.errors:
                        msg = u'%s, %s' % (field.name, field.errors[0].replace('<ul class="errorlist"><li>',''))

        else:
            msg = 'Not ajax'

        json = simplejson.dumps({'success': True, 'status': status, 'msg': msg})
        return R(json, mimetype='application/json')


    @login_required
    def accept(self, request):
        """
        Accept work
        """

        status = 'error'
        try:
            work_id = int(request.GET.get('work'))
            previous_step_id = int(request.GET.get('step'))

            P = request.POST

            try:
                # get the work
                w = Work.objects.get(pk=work_id, status='A', current_step=previous_step_id)

                # make the dynamic form
                form = self.__get_dynamicworkform(w.current_step.pk)
                f = form(P)
                if f.is_valid():
                    if P.get('step') and P.get('step') > 0:
                        w.current_step = Step.objects.get(pk=P.get('step'))
                    else:
                        w.status = 'F'

                    if previous_step_id > 0:
                        w.previous_step = Step.objects.get(pk=previous_step_id)

                    w.reject = False
                    w.reason_reject = ''
                    w.save()
                    self.__insert_work_history(w, request.user, u'Encaminhado para o passo %s.' % w.current_step.name)

                    # verify the field's name match dynamicfield
                    for k in P.keys():
                        try:
                            dynfield = DynamicFieldStep.objects.get(name=k)
                            value = P.get(k)

                            if dynfield.fieldtype == 'BooleanField':
                                value =  value == 'true' and 'Sim' or 'Nao'
                            elif dynfield.fieldtype == 'DecimalField':
                                value = value == '' and 0 or value.replace(',','.')

                            # check if there is the field on database
                            try:
                                wi = WorkFieldValue.objects.get(work=w, dynamicfield=dynfield)
                                wi.value = value
                                wi.save()
                                status = 'ok'
                                msg = 'Sucesso! Trabalho atualizado e encaminhado ao próximo passo'
                            except:
                                try:
                                    wi = WorkFieldValue.objects.create(work=w, dynamicfield=dynfield, value=value)
                                    wi.save()
                                    status = 'ok'
                                    msg = 'Sucesso! Trabalho encaminhado ao próximo passo'
                                except Exception, e:
                                    msg = e.message
                        except Exception, e:
                            # fields in post don't match
                            msg = 'Error: %s' % e.message
                else:
                    for field in f:
                        if field.errors:
                            msg = '[%s], %s' % (field.name, field.errors[0].replace('<ul class="errorlist"><li>',''))
                            break
            except Exception, e:
                msg = e.message


        except Exception, e:
            msg = e.message

        json = simplejson.dumps({'success': True, 'status': status, 'msg': msg})
        return R(json, mimetype='application/json')


    @login_required
    def reject(self, request):
        """
        Reject a work
        """

        status = 'error'
        try:
            work_id = int(request.GET.get('work'))
            step_id = int(request.GET.get('step'))
            P = request.POST

            try:
                w = Work.objects.get(pk=work_id, status='A', current_step=step_id)
                w.reason_reject = unicode(P.get('reason_reject'))
                try:
                    if w.current_step == w.previous_step:
                        msg = 'O trabalho nao pode ser recusado'
                    else:
                        w.current_step = w.previous_step
                        w.reject = True
                        w.save()
                        self.__insert_work_history(w, request.user, u'Recusado, retornando ao passo %s.' % w.current_step.name)
                        status = 'ok'
                        msg = 'O trabalho foi recusado e voltou ao passo anterior'
                except Exception, e:
                    msg = 'Nao pode ser recusado\%s' % e.message

            except Exception, e:
                msg = e.message

        except Exception, e:
            msg = e.message #return R('Nenhum trabalho em ABERTO selecionado. %s' % e.message)

        json = simplejson.dumps({'success': True, 'status': status, 'msg': msg})
        return R(json, mimetype='application/json')


    @login_required
    def history(self, request):
        """
        Get work history
        """

        if request.is_ajax():
            try:
                work_id = request.GET.get('work')
                wh = WorkHistory.objects.filter(work=work_id).order_by('-datetime_add')
                if wh.count() > 0:
                    rows = []
                    for item in wh:
                        d = {
                            #'id': item.pk,
                            'datetime_add': item.datetime_add.strftime('%d/%m/%Y %H:%M'),
                            'user': unicode(item.user),
                            'desc': item.desc,
                        }
                        rows.append(d)
                    r = {'total': len(wh.values()), 'rows': rows}
                else:
                    r = {'total': 0, 'rows': [{'id':0 , 'datetime_add': '', 'user': '', 'desc': 'Nenhum resultado'}]}
            except Exception, e:
                r = {'total': 0, 'rows': [{'id':0 , 'datetime_add': '', 'user': '', 'desc': e.message}]}

            json = simplejson.dumps(r)
            return R(json,mimetype='application/json')
        else:
            return R('Not ajax')


    @login_required
    def files(self, request):
        """
        Show work files
        """

        if request.method == 'GET':
            work_id = request.GET.get('work')
            a = Attachment.objects.filter(work=work_id, user=request.user).order_by('-datetime_change')
            return direct_to_template(request, 'files.html', extra_context={'work_id':work_id, 'files': a})
        else:
            return R('Nenhum trabalho selecionado.')


    @login_required
    def information(self, request):
        """
        Return a page about work information
        """

        try:
            work_id = int(request.GET.get('work'))

            p = ProcessFieldValue.objects.filter(work=work_id)
            p_list = []
            if p.count() > 0:
                for item in p:
                    p_list.append({
                        'label': item.dynamicfield.label,
                        'value': item.value,
                    })
            w = WorkFieldValue.objects.filter(work=work_id).order_by('dynamicfield__step__sequence')
            w_list = []
            if w.count() > 0:

                for item in w:
                    w_list.append({
                        'label': item.dynamicfield.label,
                        'value': item.value,
                        'step': u'%s' % item.dynamicfield.step,
                    })
            return direct_to_template(request, 'information.html', {'information': w_list, 'initial_fields': p_list})
            #else:
            #    return R('<p style="color:red">Nenhuma informação disponível para esse trabalho.</p>')
        except Exception, e:
            return R(e.message)

    @login_required
    def client(self, request):
        """
        Return data about client
        """

        try:
            w = Work.objects.get(id=request.GET.get('work'))
            try:
                client_id = w.client.id
                return HttpResponseRedirect('%sclient/client/objects/%s' % (settings.DATABROWSE_URL, client_id))
            except:
                return R('Não há cliente relacionado à esse trabalho.')

        except Exception, e:
            return R(e.message)


class FileView(object):
    @never_cache
    #@login_required
    def add(self, request):
        if request.method == 'POST':
            #result = {'success': True, 'msg': 'Status do trabalho = FECHADO'}
            try:
                # Nao anexa arquivos em Works fechados
                w = Work.objects.get(id=request.GET.get('work'), status='A')
                request.POST['user'] = request.user.id
                request.POST['work'] = request.GET.get('work')

                form = AttachForm(request.POST, request.FILES)
                if form.is_valid():
                    try:
                        form.save()
                        result = {'success': True, 'status': 'ok', 'msg': 'Arquivo anexado'}
                    except Exception, e:
                        msg = 'Error: ', e
                        result = {'success': True, 'status': 'error', 'msg': msg}
                else:
                    msg = 'Preencha corretamente o formulario'
                    for field in form:
                        if field.errors:
                            msg = '%s: %s' % (field.label, field.errors[0])
                    result = {'success': True, 'status': 'error', 'msg': msg}
            except: #Exception, e:
                result = {'success': True, 'status': 'error', 'msg': 'O trabalho encontra-se no status FECHADO e não permite anexar arquivos.'}



        json = simplejson.dumps(result)
        return R(json, mimetype='text/html')
        #return R(json, mimetype='application/json')


    @login_required
    def remove(self, request):
        if request.is_ajax():
            attach_id = request.GET.get('attach')
            try:
                a = Attachment.objects.get(id=attach_id, user=request.user).delete()
                if a is not None:
                    result = {'success': True, 'status': 'ok', 'msg': 'Arquivo excluido'}
                else:
                    result = {'success': True, 'status': 'error', 'msg': 'Arquivo nao foi excluido'}
            except Exception, e:
                msg = 'Error: ', e
                result = {'success': True, 'status': 'error', 'msg': msg}
        else:
            result = {'success': False, 'status': 'error', 'msg': 'Not ajax'}

        json = simplejson.dumps(result)
        return R(json, mimetype='text/html')


    @login_required
    def get(self, request):
        """
        Return the files's works for a grid
        """

        if request.is_ajax(): # == 'POST':
            try:
                work_id = int(request.GET.get('work'))
                w = Attachment.objects.filter(work=work_id).order_by('filename')
                if w.count() > 0:

                    rows = []
                    for item in w:
                        if item.user == request.user:
                            delete_class = '<center><div class="delete-abled-icon" onclick="deleteFile(%s)"></div></center>' % item.id
                        else:
                            delete_class = '<center><div class="delete-disabled-icon"></div></center>'

                        d = {
                        #
                            'id': item.pk,
                            'filename': '<a href="%s">%s</a>' % (reverse('workflow_file_download', args=[item.filename]), item.filename),
                            'datetime_change': item.datetime_change.strftime('%d/%m/%Y'),
                            'delete': delete_class
                        }
                        rows.append(d)
                    r = {'total': len(w.values()), 'rows': rows}
                else:
                    r = {'total': 0, 'rows': [{'id':0 , 'name':'Nenhum resultado'}]}
            except:
                r = {'total': 0, 'rows': [{'id':0 , 'name':'nada'}]}

            json = simplejson.dumps(r)
            return R(json,mimetype='application/json')


    @login_required
    def download(self, request, filename):
        from django.core.servers.basehttp import FileWrapper
        a = get_object_or_404(Attachment, filename=filename)
        f = a.filepath.path
        #mime = 'application/force-download'
        mime = 'application/octet-stream';
        #import mimetypes
        #mime = mimetypes.guess_type(filename)[0]
        try:
            wrapper = FileWrapper(file(f))
            response = R(wrapper, mimetype=mime)
            response['Content-Disposition'] = 'inline; filename="%s"' % filename
            response['Content-Length'] = os.path.getsize(f)
            return response
        except:
            return R('Erro: Arquivo n&atilde;o encontrado no servidor.')

class ItemView(object):

    @login_required
    def add(self, request):
        if request.method == 'POST':
            try:
                w = Work.objects.get(id=request.POST.get('work'))
                if not w.owner == request.user:
                    result = {'success': True, 'status': 'error', 'msg': 'Permissão negada.<br>Apenas o dono do trabalho pode alterar a tabela.'}
                else:
                    items = simplejson.loads(request.POST.get('items'))
                    if len(items) > 0:
                        for items_dict in items:
                            try:
                                i = Item.objects.get(id=items_dict['id'])
                            except:
                                i = Item()
                            i.work = w
                            i.user = request.user
                            i.product = Product.objects.get(pk=items_dict['product'])
                            i.productprice = ProductPrice.objects.get(productservice=items_dict['productservice'])
                            i.amount = items_dict['amount']
                            i.price = str(items_dict['price'])
                            try:
                                i.save()
                                result = {'success': True, 'status': 'ok', 'msg': 'Tabela salva com sucesso.'}
                            except Exception, e:
                                result = {'success': True, 'status': 'error', 'msg': e.message}
            except Exception, e:
                result = {'success': True, 'status': 'error', 'msg': e.message}

        json = simplejson.dumps(result)
        return R(json, mimetype='text/html')


    @login_required
    def get(self, request):
        """
        Return the items
        """

        if request.is_ajax(): # == 'POST':
            try:
                work_id = int(request.GET.get('work'))
                i = Item.objects.filter(work=work_id).order_by('product')
                if i.count() > 0:
                    rows = []
                    for item in i:
                        #if item.user == request.user:
                        #    delete_class = '<center><div class="delete-abled-icon" onclick="deleteFile(%s)"></div></center>' % item.id
                        #else:
                        #    delete_class = '<center><div class="delete-disabled-icon"></div></center>'
                        d = {
                            'id': item.pk,
                            'product': item.product.id,
                            'productservice': item.productprice.productservice.id,
                            'amount': item.amount,
                            'price': str(item.price),
                            'grouping': 'Itens'
                        }
                        rows.append(d)
                    r = {'total': len(i.values()), 'rows': rows}
                else:
                    r = {'total': 0, 'rows': [{'id':0 , 'name':'Nenhum resultado', 'grouping': 'Itens'}]}
            except Exception, e:
                r = {'total': 0, 'rows': [{'id':0 , 'name':e.message}]}

            json = simplejson.dumps(r)
            return R(json,mimetype='application/json')


    @login_required
    def remove(self, request):
        if request.is_ajax():
            item_id = request.POST.get('id')
            try:
                i = Item.objects.get(id=item_id, user=request.user).delete()
                result = {'success': True, 'status': 'ok', 'msg': 'Item removido'}
            except:
                result = {'success': True, 'status': 'error', 'msg': 'Permissão negada'}
        else:
            result = {'success': False, 'status': 'error', 'msg': 'Not ajax'}

        json = simplejson.dumps(result)
        return R(json, mimetype='text/html')

    @login_required
    def products(self, request):
        """
        Return the product list for combobox
        """

        if request.is_ajax(): # == 'POST':
            try:
                p = Product.objects.all()
                if p.count() > 0:
                    rows = []
                    for item in p:
                        try:
                            product_with_price = item.productprice_set.select_related().filter(price__gt=0)
                            if product_with_price.count() > 0:
                                d = {'id': item.pk, 'name': item.name}
                                rows.append(d)
                        except:
                            pass
                    r = {'total': len(rows), 'rows': rows}
                else:
                    r = {'total': 0, 'rows': [{'id':0 , 'name':'Nenhum resultado'}]}
            except Exception, e:
                r = {'total': 0, 'rows': [{'id':0 , 'name':e.message}]}

            json = simplejson.dumps(r)
            return R(json,mimetype='application/json')


    @login_required
    def report(self, request):
        if request.method == 'GET':
            work_id = request.GET.get('work')
            try:
                w = Work.objects.get(id=work_id)
                fields = w.processfieldvalue_set.all().order_by('dynamicfield')
                field_list = {}
                for item in fields:
                    field_list.update({
                        #'field': item.dynamicfield.label,
                        #'value': item.value
                        item.dynamicfield.name.replace('-',''): [item.value, '-'][item.value == '' or item.value == None]
                    })

                item_list = []
                total = 0
                for item in w.item_set.all():
                    item_list.append({
                        'product': item.product.name,
                        'product_desc': item.product.desc,
                        'amount': item.amount,
                        'price': item.price,
                        'total': item.total
                    })
                    total += item.total
                context = {
                    'work': w,
                    'fields': field_list,
                    'items': item_list,
                    'total': total,
                    'pagesize' : 'A4'
                }
                return write_pdf('report_pedido.html', context, 'pedido%s' % work_id)
                #return direct_to_template(request, 'report_pedido.html', extra_context=context)

            except Exception, e:
                return R('Nenhum trabalho selecionado<br>%s' % e.message)

