from django.conf.urls.defaults import patterns, url

from viperdb.views.add_entry import (StepOneView, StepTwoView, StepThreeView,
                                     StepFourView, StepFiveView)

urlpatterns = patterns("viperdb.views.add_entry",
    url(r"^$", StepOneView.as_view(), name="step_one"),
    url(r"^step_two$",   StepTwoView.as_view(),   name="step_two"),
    url(r"^step_three$", StepThreeView.as_view(), name="step_three"),
    url(r"^step_four$",  StepFourView.as_view(),  name="step_four"),
    url(r"^step_five$",  StepFiveView.as_view(),  name="step_five"),
    url(r"^start_pdbase$", "start_pdbase", name="start_pdbase"),
)
