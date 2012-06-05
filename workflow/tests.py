# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from workflow.models import *

class WorkflowTest(TestCase):
    fixtures = ['auth.json', 'workflow.json']
    def setUp(self):
        """
        Constructor
        """

        self.c = Client()
        self.jsonResultOk = '"status": "ok"' #, "success": true}'
        logged = self.c.login(username='usuario1',password='usuario1')
        self.failUnlessEqual(logged, True)


class WorkTest(WorkflowTest):
    def _addWork(self, name, desc):
        """
        Add new work with the process 1
        """

        c = self.c
        response = c.post(u'%s?process=1' % reverse('workflow_work_add'), {'name':name, 'desc':desc}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        #return self.failUnlessEqual(response.content, self.jsonResultOk)
        self.assertContains(response, self.jsonResultOk)


    def addWorkValid(self):
        """
        Add valid work
        """

        self._addWork('trabalho1', 'descrição1')


    def acceptWork(self):
        """
        Accept work from step1 to step2
        """

        c = self.c

        # create a work passing the process id in url
        response = c.post(u'%s?process=1' % reverse('workflow_work_add'), {'name':'Trabalho2', 'desc':'Descricao2'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data_post = {
          'texto': 'HelloWorld',
          'numinteiro': '100',
          'data': '08/01/1984',
          'email': 'gustavo@gustavohenrique.net',
          'numdecimal': '11.22',
          'simounao': True,
          'step': 2,
        }

        # pass the work id and current step in url
        response = c.post(u'%s?work=1&step=1' % reverse('workflow_work_accept'), data_post) #, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        #return self.failUnlessEqual(response.content, self.jsonResultOk)
        self.assertContains(response, self.jsonResultOk)
        #print response.content


    def rejectWork(self):
        """
        Reject work in step2
        """

        c = self.c

        # create a work passing the process id in url
        response = c.post(u'%s?process=1' % reverse('workflow_work_add'), {'name':'Trabalho2', 'desc':'Descricao2'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, self.jsonResultOk)

        # accept work from step1 to step2
        data_post = {
          'texto': 'Texto aqui',
          'numinteiro': '100',
          'data': '08/01/1984',
          'email': 'gustavo@gustavohenrique.net',
          'numdecimal': '11.22',
          'simounao': True,
          'step': 2,
        }
        response = c.post(u'%s?work=1&step=1' % reverse('workflow_work_accept'), data_post, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, self.jsonResultOk)

        # reject work in step2 back to step1
        data_post = {'reason_reject': 'Informacoes insuficientes'}
        response = c.post(u'%s?work=1&step=2' % reverse('workflow_work_reject'), data_post)
        #self.failUnlessEqual(response.content, self.jsonResultOk)
        self.assertContains(response, self.jsonResultOk)


class ProcessTest(WorkflowTest):
    def getInformation(self):
        c = self.c
        response = c.post(reverse('workflow_process_info'), {'step':1}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, '"status": "ok"', 1, 200)


class FileTest(WorkflowTest):
    def addAndRemoveFile(self):
        c = self.c
        # create a work passing the process id in url
        response = c.post(u'%s?process=1' % reverse('workflow_work_add'), {'name':'Tarefa principal', 'desc':'Sem descricao'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, self.jsonResultOk)

        f = open('/tmp/x.txt')
        response = c.post(u'%s?work=1' % reverse('workflow_file_add'), {'filepath': f})
        self.assertContains(response, '"status": "ok"', 1, 200)

        response = c.post(u'%s?attach=1' % reverse('workflow_file_del'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        print response.content
        #self.assertContains(response, '"status": "ok"', 1, 200)






__test__ = {"doctest": """
#>>> import sys
#>>> from django.test.client import Client
#>>> from django.contrib.auth.models import User
#>>> user = User.objects.create_user('gustavo', 'gustavo@gustavohenrique.net', 'henrique').save()
#>>> c = Client()
#>>> c.login(username='gustavo',password='henrique')
#True
#>>> response = c.post('/workflow/step/works/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
#>>> response.status_code
#200
#>>> #print response.content
"""}
