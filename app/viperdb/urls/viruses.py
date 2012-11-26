from django.conf.urls.defaults import patterns, url
from viperdb.views.add_entry import StepOneView, StepTwoView

urlpatterns = patterns("viperdb.views.add_entry",
    url(r"^add_entry$", StepOneView.as_view(), name="step_one"),
    # url(r"^add_entry/step_two/(?entry_id<P>[a-z0-9]{4})$",   "step_two",   name="step_two"),
    url(r"^add_entry/step_two/(?P<entry_id>[a-z0-9]{4})$", StepTwoView.as_view(), name="step_two"),
    url(r"^add_entry/step_three/(?P<entry_id>[a-z0-9]{4})$", "step_three", name="step_three"),
    url(r"^add_entry/step_four/(?P<entry_id>[a-z0-9]{4})$",  "step_four",  name="step_four"),
    url(r"^add_entry/step_five/(?P<entry_id>[a-z0-9]{4})$",  "step_five",  name="step_five"),
    url(r"^add_entry/start_pdbase$", "start_pdbase", name="start_pdbase"),
)

urlpatterns += patterns("viperdb.views.viruses",
    url(r"^$", "index", name="index"),
    url(r"^(?P<entry_id>[a-zA-Z0-9]{4})$",                   "info", name="info"),
    url(r"^(?P<entry_id>[a-zA-Z0-9]{4})/phi_psi$",           "phi_psi", name="phi_psi"),
)

