from django import forms

from celery.execute import send_task

from viperdb.models import Virus, Layer, Entity, Family
from viperdb.helpers import pdb_exists





class InitialVirusForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.update({"initial":{"file_source": 1}})
        super(InitialVirusForm, self).__init__(*args, **kwargs)
        
        for key, field in self.fields.iteritems():
            if field.required:
                field.widget.attrs.update({'class':'required'})
    FILE_REMOTE = 1
    FILE_LOCAL = 2
    FILE_UPLOAD = 3
    FILE_SOURCE_CHOICES = ((FILE_REMOTE, 'Use up-to-date PDB and CIF files from RCSB'),
                           (FILE_LOCAL, 'Use existing PDB and CIF files on VIPERdb'),)
                           # (FILE_UPLOAD, 'Upload your own PDB and CIF files to VIPERdb'))
    
    entry_id = forms.CharField(max_length=8)
    file_source = forms.ChoiceField(widget=forms.RadioSelect, choices=FILE_SOURCE_CHOICES)
    # pdb_file_upload = forms.FileField(required=False)
    # cif_file_upload = forms.FileField(required=False)

    def clean(self):
        file_source = int(self.cleaned_data["file_source"])
        entry_id= self.cleaned_data["entry_id"]

        if file_source == self.FILE_REMOTE:
            if not pdb_exists(entry_id):
                raise forms.ValidationError("PDB id does not exist in RCSB.")
        elif file_source == self.FILE_LOCAL:
            task = send_task('virus.check_file_count', args=[entry_id])

            if task.get() is not 2:                
                raise forms.ValidationError("PDB and/or CIF file not found locally.")
        elif file_source == self.FILE_UPLOAD:
            pass

        return self.cleaned_data


class VirusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VirusForm, self).__init__(*args, **kwargs)
        self.fields["family"].queryset = Family.objects.order_by('name')
        for key, field in self.fields.iteritems():
            if field.required:
                field.widget.attrs.update({'class':'required'})

    class Meta:
        model = Virus
        widgets = {}
        exclude = ['entry_key', 'prepared', 'layer_count']

    def clean(self):
        return self.cleaned_data

class LayerForm(forms.ModelForm):
    def __init__(self, entry_key, *args, **kwargs):
        super(LayerForm, self).__init__(*args, **kwargs)
        self.fields['entities'] = forms.ModelMultipleChoiceField(
            queryset=Entity.objects.filter(entry_key=entry_key, 
                                           type='polymer'),
            widget=forms.CheckboxSelectMultiple,
        )
        for key, field in self.fields.iteritems():
            if field.required:
                field.widget.attrs.update({'class':'required'})


    class Meta:
        model = Layer
        exclude = ['entry_key', 'layer_id', 'entry_id', "min_diameter", "ave_diameter", "max_diameter"]

    def clean(self):
        return self.cleaned_data

class MatrixChoiceForm(forms.Form):
    MTX_VIPERIZE = 1
    MTX_INPUT = 2
    MTX_UNIT = 3
    MATRIX_CHOICES = ((MTX_VIPERIZE,'Use viperize to generate PDB to VIPER matrix'),
                      (MTX_INPUT, 'Input your own matrix'),
                      (MTX_UNIT, 'Use Unix Matrix'))
    
    matrix_selection = forms.ChoiceField(widget=forms.RadioSelect, choices=MATRIX_CHOICES)

class ChainForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.update({"initial":{"chain_selection": 1}})
        kwargs.update({"empty_permitted":False})
        super(ChainForm, self).__init__(*args,**kwargs)

    chain_selection = forms.ChoiceField(widget=forms.RadioSelect, choices=Virus.CHAIN_CHOICES)
    chain_input = forms.CharField(max_length=2, required=False)

class MoveChainForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.update({"initial":{"move_selection": 1}})
        super(MoveChainForm, self).__init__(*args, **kwargs)

    MOVE_NONE = 1
    MOVE_ALL  = 2
    move_choices = ((MOVE_NONE, "Move none"), (MOVE_ALL, "Move all chains"))
    move_selection = forms.ChoiceField(widget=forms.RadioSelect, choices=move_choices)
    matrix_selection = forms.IntegerField(min_value=1, max_value=60, required=False)

class ImageAnalysisForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.update({"initial":{"analysis_selection": 1}})
        super(ImageAnalysisForm, self).__init__(*args, **kwargs)

    BOTH_IMAGE_AND_ANALYSIS = 1
    ANALYSIS_ONLY = 2
    IMAGE_ONLY = 3
    NO_ACTION = 4

    analysis_choices = (
        (BOTH_IMAGE_AND_ANALYSIS, "Perform analysis and generate images."),
        (ANALYSIS_ONLY, "Perform analysis only."),
        (IMAGE_ONLY, "Generate images only."),
        (NO_ACTION, "Do nothing.")
    )
    analysis_selection = forms.ChoiceField(widget=forms.RadioSelect, 
                                           choices=analysis_choices)


