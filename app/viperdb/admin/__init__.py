from django.contrib import admin

from viperdb.views.add_entry import StepOneView
from viperdb.models import Virus
from viperdb.admin.virus import VirusAdmin

admin.site.register(Virus, VirusAdmin)
