from settings import PROJECT_DIR
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^discursos/(?P<keyword>[a-z]*)/(?P<argument>.*)/$', 'dashboard.views.filtro'),
    (r'^taggeia/', 'dashboard.views.taggeia'),
    #(r'^discursos/', 'dashboard.views.index'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #Static Files
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': PROJECT_DIR + '/../static','show_indexes': True}),
)
