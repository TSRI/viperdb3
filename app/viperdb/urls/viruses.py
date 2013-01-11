from django.conf.urls.defaults import patterns, url
from viperdb.views.add_entry import StepOneView, StepTwoView, StepThreeView

urlpatterns = patterns("viperdb.views.add_entry",
    url(r"^add_entry$", StepOneView.as_view(), name="step_one"),
    url(r"^add_entry/step_two$", StepTwoView.as_view(), name="step_two"),
    url(r"^add_entry/step_three$", StepThreeView.as_view(), name="step_three"),
    url(r"^add_entry/step_four$",  "step_four",  name="step_four"),
    url(r"^add_entry/step_five$",  "step_five",  name="step_five"),
    url(r"^add_entry/start_pdbase$", "start_pdbase", name="start_pdbase"),
)

urlpatterns += patterns("viperdb.views.viruses",
    url(r"^$", "index", name="index"),
    url(r"^(?P<entry_id>[a-zA-Z0-9]{4})$",                   "info", name="info"),
    url(r"^(?P<entry_id>[a-zA-Z0-9]{4})/phi_psi$",           "phi_psi", name="phi_psi"),
)

