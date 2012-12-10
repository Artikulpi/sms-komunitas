from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^settings/age/$', 'member.views.settings_age', name='setting_age'),
    url(r'^settings/age/(?P<age_id>\d+)/$', 'member.views.view_age'),
    url(r'^settings/age/(?P<age_id>\d+)/delete/$', 'member.views.delete_age'),
    
    url(r'^settings/social/$', 'member.views.settings_social', name='setting_social'),
    url(r'^settings/social/(?P<sos_id>\d+)/$', 'member.views.view_social'),
    url(r'^settings/social/(?P<sos_id>\d+)/delete/$', 'member.views.delete_social'),
    
    url(r'^$', 'member.views.home', name='member'),
    url(r'^(?P<member_id>\d+)/$', 'member.views.view_member'),
)