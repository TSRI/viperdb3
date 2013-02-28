from django.conf.urls.defaults import patterns, url

from viperdb.views.viruses import VirusInfoView, VirusListView

urlpatterns = patterns("viperdb.views.viruses",
    url(r"^$", VirusListView.as_view(), name="index"),
    url(r"^(?P<entry_id>[a-zA-Z0-9]{4})$", VirusInfoView.as_view(), name="info"),
    url(r"^(?P<entry_id>[a-zA-Z0-9]{4})/phi_psi$",           "phi_psi", name="phi_psi"),
)
