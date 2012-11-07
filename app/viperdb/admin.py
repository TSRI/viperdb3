from django.contrib import admin
from adminplus import AdminSitePlus
from viperdb.views.add_entry import AddEntryView

admin.site = AdminSitePlus()

admin.site.register_view("add_entry", AddEntryView.as_view(), "Add a new entry")