# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from workflow.views import WorkView, ProcessView, FileView, ItemView

urlpatterns = patterns('workflow.views',
    url(r'^$', 'index', name='workflow_index'),
    url(r'^menu/$', 'menu', name='workflow_menu'),
    url(r'^step/tasks/$', 'get_step_tasks', name='workflow_step_tasks'),

)

"""
Works
"""
urlpatterns += patterns('',
    url(r'^work/get/$', WorkView().get, name='workflow_work_get'),
    url(r'^work/new/$', WorkView().new, name='workflow_work_new'),
    url(r'^work/add/$', WorkView().add, name='workflow_work_add'),
    url(r'^work/accept/$', WorkView().accept, name='workflow_work_accept'),
    url(r'^work/reject/$', WorkView().reject, name='workflow_work_reject'),
    url(r'^work/history/$', WorkView().history, name='workflow_work_history'),
    url(r'^work/files/$', WorkView().files, name='workflow_work_files'),
    url(r'^work/form/accept/$', WorkView().form_accept, name='workflow_work_form_accept'),
    url(r'^work/information/$', WorkView().information, name='workflow_work_information'),
    url(r'^work/client/$', WorkView().client, name='workflow_work_client'),

)

"""
Process
"""
urlpatterns += patterns('',
    url(r'^process/get/work/$', ProcessView().work, name='workflow_process_work'),
)

"""
Files
"""
urlpatterns += patterns('',
    url(r'^file/add/$', FileView().add, name='workflow_file_add'),
    url(r'^file/get/$', FileView().get, name='workflow_file_list'),
    url(r'^file/del/$', FileView().remove, name='workflow_file_del'),
    #url(r'^file/download/(?P<filename>.*?)/$', FileView().download, name='workflow_file_download'),
    url(r'^file/download/(?P<filename>[a-zA-Z0-9_.-]+)/$', FileView().download, name='workflow_file_download'),
)

"""
Item
"""
urlpatterns += patterns('',
    url(r'^item/add/$', ItemView().add, name='workflow_item_add'),
    url(r'^item/get/$', ItemView().get, name='workflow_item_list'),
    url(r'^item/del/$', ItemView().remove, name='workflow_item_del'),
    url(r'^item/products/$', ItemView().products, name='workflow_item_products'),
    url(r'^item/report/pedido/$', ItemView().report, name='workflow_item_report'),
)
