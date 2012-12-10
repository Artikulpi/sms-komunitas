from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^xhr/dusun/(?P<id_desa>\d+)/$', 'wilayah.views.xhr_dusun'),
    url(r'^xhr/kampung/(?P<id_dusun>\d+)/$', 'wilayah.views.xhr_kampung'),
)

