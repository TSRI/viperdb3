from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',          'viperdb.views.misc.home', name='home'),
    url(r'^admin/',     include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^viruses/',     include('viperdb.urls.viruses', namespace='virus', 
                                app_name='viperdb')),
    url(r'^family/',    include('viperdb.urls.families', namespace='family', 
                                app_name='viperdb')),
    url(r'^api/',       include('api.urls', namespace='api')),
)

urlpatterns += staticfiles_urlpatterns()