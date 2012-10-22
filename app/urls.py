from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',          'viperdb.views.home', name='home'),
    url(r'^admin/',     include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^virus/',     include('viperdb.virus.urls', namespace='virus', app_name='virus')),
    url(r'^family/',    include('viperdb.family.urls', namespace='family', app_name='family')),
    url(r'^api/',       include('viperdb.api.urls', namespace='api')),
)

urlpatterns += staticfiles_urlpatterns()