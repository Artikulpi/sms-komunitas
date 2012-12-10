from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login',
            {'template_name': 'accounts/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^profile/$', 'accounts.views.profile'),
    
    url(r'^admin/$', 'accounts.views.admin', name='user_admin'),
    url(r'^admin/new/$', 'accounts.views.new'),
    url(r'^admin/(?P<user_id>\d+)/$', 'accounts.views.view_account'),
    url(r'^admin/(?P<user_id>\d+)/delete/$', 'accounts.views.delete_account'),
    url(r'^admin/(?P<user_id>\d+)/password/$', 'accounts.views.change_password'),
)
