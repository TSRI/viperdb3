
from django import forms

from viperdb.models import Virus

class OligomerModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s (T=%s)" % (obj.entry_id, obj.name, obj.get_tnumber())

class OligomerGeneratorForm(forms.Form):
    NONE       = 0
    FULL       = 1
    TWOTHIRDS  = 2
    HALF       = 3
    ONETHIRD   = 4
    ONEQUARTER = 5
    SECTION_CHOICES = (
        (NONE,       "NO"),
        (FULL,       "60mer (full)"),
        (TWOTHIRDS,  "40mer (2/3)"),
        (HALF,       "30mer (1/2)"),
        (ONETHIRD,   "20mer (1/3)"),
        (ONEQUARTER, "15mer (1/4)"),
    )

    BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
    entry = OligomerModelChoiceField(queryset=Virus.objects.all(), required=False)
    file_upload = forms.FileField(required=False)
    section_selection = forms.ChoiceField(choices=SECTION_CHOICES)
    use_c_alpha = forms.TypedChoiceField(widget=forms.RadioSelect, choices=BOOL_CHOICES, coerce=int)
    for_modeller = forms.TypedChoiceField(widget=forms.RadioSelect, choices=BOOL_CHOICES, coerce=int)
