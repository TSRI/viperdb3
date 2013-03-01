from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',          'viperdb.views.misc.home', name='home'),
    url(r'^admin/add_entry/', include('viperdb.urls.add_entry', 
                                      namespace='add_entry', 
                                      app_name='viperdb')),
    url(r'^admin/',     include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^viruses/',     include('viperdb.urls.viruses', namespace='viruses', 
                                app_name='viperdb')),
    url(r'^families/',    include('viperdb.urls.families', namespace='families', 
                                app_name='viperdb')),
    url(r'^api/',       include('api.urls', namespace='api')),
    url(r'^utilities/', include('viperdb.urls.utilities', namespace='utilities',
                                app_name='viperdb')),
)

urlpatterns += staticfiles_urlpatterns()