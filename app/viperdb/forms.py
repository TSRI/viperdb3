from django import forms
from models import Virus, Layer

class InitialVirusForm(forms.Form):
    FILE_REMOTE = 1
    FILE_LOCAL = 2
    FILE_UPLOAD = 3
    FILE_SOURCE_CHOICES = ((FILE_REMOTE, 'Use up-to-date PDB and CIF files from RCSB'),
                           (FILE_LOCAL, 'Use existing PDB and CIF files on VIPERdb'),
                           (FILE_UPLOAD, 'Upload your own PDB and CIF files to VIPERdb'))
    
    entry_id = forms.CharField(max_length=8)
    file_source = forms.ChoiceField(widget=forms.RadioSelect, choices=FILE_SOURCE_CHOICES)
    pdb_file_upload = forms.FileField(required=False)
    cif_file_upload = forms.FileField(required=False)

    def clean(self):
        return self.cleaned_data

class VirusForm(forms.ModelForm):
    class Meta:
        model = Virus
        widgets = {}
        exclude = ['entry_key', 'prepared', 'layer_count']

    def clean(self):
        return self.cleaned_data

class LayerForm(forms.ModelForm):
    class Meta:
        model = Layer
        exclude = ['entry_key', 'layer_id', 'entry_id', "min_diameter", "ave_diameter", "max_diameter"]

class MatrixChoiceForm(forms.Form):
    matrix_selection = forms.ChoiceField(widget=forms.RadioSelect, choices=Virus.MATRIX_CHOICES)

class ChainForm(forms.Form):
    chain_selection = forms.ChoiceField(widget=forms.RadioSelect, choices=Virus.CHAIN_CHOICES)
    chain_input = forms.CharField(max_length=2, required=False)

class MoveChainForm(forms.Form):
    MOVE_NONE = 1
    MOVE_ALL  = 2
    move_choices = ((MOVE_NONE, "Move none"), (MOVE_ALL, "Move all chains"))
    move_selection = forms.ChoiceField(widget=forms.RadioSelect, choices=move_choices)
    matrix_selection = forms.IntegerField(min_value=1, max_value=60, required=False)

class ImageAnalysisForm(forms.Form):
    IMAGE_ONLY = 1
    ANALYSIS_ONLY = 2
    BOTH_IMAGE_AND_ANALYSIS = 3
    NO_ACTION = 4
    analysis_choices = (
        (IMAGE_ONLY, "Generate images only."),
        (ANALYSIS_ONLY, "Perform analysis only."),
        (BOTH_IMAGE_AND_ANALYSIS, "Perform analysis and generate images."),
        (NO_ACTION, "Do nothing.")
    )
    analysis_selection = forms.ChoiceField(widget=forms.RadioSelect, 
                                           choices=analysis_choices)

