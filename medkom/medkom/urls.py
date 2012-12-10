from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'message.views.home', name='home'),
    url(r'^messages/', include('message.urls')),
    url(r'^wilayah/', include('wilayah.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^member/', include('member.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
