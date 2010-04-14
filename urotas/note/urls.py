from django.conf.urls.defaults import *

urlpatterns = patterns('note.views',
    (r'^$', 'index'),
    (r'^create$', 'create'),
    (r'^modify$', 'modify'),
    (r'^remove$', 'remove'),
    (r'^list/$', 'list'), # FIXME two similar url patterns?
    (r'^list/(?P<format>json)?$', 'list'),
)
