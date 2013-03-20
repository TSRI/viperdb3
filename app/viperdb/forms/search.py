from django import forms
from viperdb.models import Virus, Layer

class SearchForm(forms.Form):
    family = forms.ModelChoiceField(queryset= Virus.objects.values('family').distinct())
    tnumber = forms.ModelChoiceField(queryset = Layer.objects.values('tnumber').distinct())
    cryo = forms.BooleanField()
