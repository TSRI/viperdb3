from django.core.urlresolvers import reverse
from django.db.models import Min, Max
from django.shortcuts import redirect
from django.views.generic import FormView

from annoying.functions import get_object_or_None
from celery.execute import send_task

from viperdb.forms.add_entry import MoveChainForm, ImageAnalysisForm
from viperdb.models import Virus, AtomSite, IcosMatrix, AuMatrix, MmsEntry

class StepFourView(FormView):
    template_name = "add_entry/step_four.html"
    form_class = MoveChainForm

    def get_context_data(self, **kwargs):
        virus = Virus.objects.get(pk=self.request.session['entry_id'])
        diameters = get_diameters(virus)

        context = super(StepFourView, self).get_context_data(**kwargs)
        context.update({
            'form': self.get_form(self.form_class),
            'ia_form': ImageAnalysisForm(),
            'diameters': diameters,
        })
        return context

    def post(self, request, *args, **kwargs):
        self.virus = Virus.objects.get(pk=request.session['entry_id'])
        self.diameters = get_diameters(self.virus)

        self.chains = (AtomSite.objects
                    .filter(entry_key=self.virus.entry_key)
                    .values('label_asym_id').distinct())
        form = self.get_form(self.form_class)
        ia_form = self.get_form(ImageAnalysisForm)

        if form.is_valid() and ia_form.is_valid():
            return self.form_valid(form, ia_form)
        else:
            return self.form_invalid(form, ia_form)

    def form_valid(self, form, ia_form):
        entry_id = self.request.session['entry_id']

        if int(form.cleaned_data['move_selection']) == MoveChainForm.MOVE_ALL:
            for chain in self.chains:
                au_matrix = move_chain(self.virus, chain['label_asym_id'], 
                                       int(form.cleaned_data['matrix_selection']))
                au_matrix.save()
            send_task('virus.make_vdb', args=[entry_id], kwargs={})
            return redirect(reverse("add_entry:step_four"))
        else:
            save_diameters(self.virus, self.diameters)

            ia_choice = int(ia_form.cleaned_data['analysis_selection'])
            if ia_choice == ImageAnalysisForm.IMAGE_ONLY:
                self.virus.generate_images()
            elif ia_choice == ImageAnalysisForm.ANALYSIS_ONLY:
                self.virus.analyze()
            elif ia_choice == ImageAnalysisForm.BOTH_IMAGE_AND_ANALYSIS:
                self.virus.analyze()
                self.virus.generate_images()
            elif ia_choice == ImageAnalysisForm.NO_ACTION:
                pass

            return redirect(reverse("add_entry:step_five"))

    def form_invalid(self, form, ia_form):
        return redirect(reverse("add_entry:step_four"))


def move_chain(virus, chain, matrix_number):
    """Moving chains from one orientation to another"""
    seq_range = AtomSite.objects.filter(
        entry_key=virus.entry_key, 
        label_asym_id=chain).aggregate(Min('auth_seq_id'), Max('auth_seq_id'))
    icos_matrix = IcosMatrix.objects.get(pk=matrix_number)
    entity_key = AtomSite.objects.filter(label_asym_id=chain, entry_key=virus.entry_key).distinct().order_by('label_asym_id')[0].label_entity_key
    au_matrix = get_object_or_None(AuMatrix, entry_id=virus.entry_id)
    if not au_matrix:
        au_matrix = AuMatrix(au_matrix_key=AuMatrix.objects.count()+1, entry_key=MmsEntry.objects.get(pk=virus.entry_key), entry_id=virus, label_entity_key=entity_key, label_asym_id=chain, seq_range_string=str(seq_range['auth_seq_id__min']) + "-" + str(seq_range['auth_seq_id__max']))

    [[setattr(au_matrix, 'matrix_' + str(i) + '_' + str(j), getattr(icos_matrix, 'matrix_' + str(i) + '_' + str(j))) for j in range(3)] for i in range(3)]
    [[setattr(au_matrix, 'matrix_%s_%s' % (str(i), str(j)), getattr(icos_matrix, 'matrix_%s_%s' % (str(i), str(j)))) for j in range(3)] for i in range(3)]
    [setattr(au_matrix, 'vector_%s' % (str(i)), 0) for i in range(3)]
    return au_matrix

def prepare_diameters(layer, diameters):
    """Prepare layer with diameter information"""
    diameter_types = ["min", "ave", "max"]
    for index, diameter in enumerate(diameters):
        setattr(layer, "%s_diameter" % (diameter_types[index]), diameter)

def get_diameters(virus):
    """Calls script to return diameters"""
    # TODO - Add logic to re-use existing diameters
    return send_task('virus.get_diameters', args=[virus.entry_id], kwargs={}).get()

def save_diameters(virus, diameters):
    """Sets diameters for given virus"""
    # TODO - Add logic for multiple layers    
    for layer in virus.layers.all():
        # diameters = get_diameters(virus)
        # if diameters:
        prepare_diameters(layer, diameters)
        layer.save()