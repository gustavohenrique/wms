from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from django.contrib import databrowse
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^databrowse/(.*)', login_required(databrowse.site.root)),

    (r'^$','django.views.generic.simple.redirect_to',  {'url': settings.LOGIN_URL}),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^workflow/', include('workflow.urls'))
)

urlpatterns += patterns('',
    url(r'^%s$' % settings.LOGIN_URL,'django.contrib.auth.views.login', name='auth_login'),
    url(r'^%s$' % settings.LOGOUT_URL,'django.contrib.auth.views.logout', name='auth_logout'),
)

if settings.DEBUG == True:
    urlpatterns += patterns('',
        (r'^media/(.*)','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    )
