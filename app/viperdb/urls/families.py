from django.conf.urls.defaults import patterns, url
from viperdb.views.utilities import SearchView

urlpatterns = patterns("viperdb.views.families",
    url(r"^$",                           SearchView.as_view(), name="index"),
    url(r"^(?P<family_name>\w+)$",       "info", name="info"),
    url(r"^(?P<family_name>\w+)/graph$", "graph", name="graph"),
)

