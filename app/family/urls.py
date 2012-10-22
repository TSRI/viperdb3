from django.conf.urls.defaults import patterns, url

urlpatterns = patterns("viperdb.family.views",
    url(r"^$",                           "index", name="index"),
    url(r"^(?P<family_name>\w+)$",       "info", name="info"),
    url(r"^(?P<family_name>\w+)/graph$", "graph", name="graph"),
)

