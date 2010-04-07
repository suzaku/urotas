from django.conf.urls.defaults import *

urlpatterns = patterns('people.views',
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout', {'template_name': 'people/logout.html'}),
    (r'^register/$', 'register'),
)
