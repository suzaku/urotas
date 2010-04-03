from django.conf.urls.defaults import *

urlpatterns = patterns('note.views',
    (r'^$', 'index'),
    (r'^create$', 'create'),
    (r'^remove$', 'remove'),
    (r'^list$', 'list'),
    (r'^search$', 'search'),
)
