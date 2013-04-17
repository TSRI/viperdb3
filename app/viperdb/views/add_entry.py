import os, subprocess

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView
from django.utils.functional import curry

from annoying.decorators import render_to, ajax_request
from annoying.functions import get_object_or_None
from celery.execute import send_task
from celery.task.sets import subtask

from viperdb.forms.add_entry import (InitialVirusForm, LayerForm, VirusForm, 
                           MatrixChoiceForm, ChainForm, MoveChainForm,
                           ImageAnalysisForm)
from viperdb.models import (MmsEntry, Virus, Entity, StructRef, LayerEntity, 
                            AtomSite, Layer)
from viperdb.helpers import get_mismatched_chains


class StepOneView(FormView):
    template_name = "add_entry/step_one.html"
    form_class = InitialVirusForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StepOneView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('add_entry:step_two')

    def get_context_data(self, **kwargs):
        context = super(StepOneView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        entry_id = form.cleaned_data['entry_id']

        virus = get_object_or_None(MmsEntry, id=entry_id)
        if virus:
            delete_existing_entry(virus)

        pdb_file_source = int(form.cleaned_data["file_source"])
        if pdb_file_source == InitialVirusForm.FILE_REMOTE:
            send_task("virus.get_pdb_files", args=[entry_id]).get()
                      # kwargs={'callback': subtask('virus.run_pdbase')})
        elif pdb_file_source == InitialVirusForm.FILE_LOCAL:
            task = send_task('virus.check_file_count', args=[entry_id], 
                             kwargs={})
            if task.get() is not 2:
                return redirect(reverse('add_entry:step_one'))
            # else:
            #     send_task('virus.run_pdbase', args=[entry_id], kwargs={})
        elif pdb_file_source == InitialVirusForm.FILE_UPLOAD:
            # TODO: allow for file upload
            pass
#                task = send_task('virus.check_file_count', args=[entry_id], kwargs={})
#                if not task.get():
#                    pdb_file = request.FILES['pdb_file_upload']
#                    cif_file = request.FILES['cif_file_upload']
#                    if pdb_file and cif_file:
#                        send_task('virus:handle_pdb_files', args=[entry_id, pdb_file, cif_file], kwargs={})
#                    else:
#                        return redirect(reverse('virus:initial_virus'))
#                else:
#                    return redirect(reverse('virus:initial_virus'))
        # send_task('virus.run_pdbase', args=[entry_id], kwargs={})
        # TODO: options to forgo analysis.

        self.request.session['entry_id'] = entry_id

        return super(StepOneView, self).form_valid(form)

@ajax_request
def delete_existing_entry(mms_entry):
    """Takes care of deleting all existing references to this virus"""
    virus = get_object_or_None(Virus, entry_key=mms_entry.entry_key)

    path = os.getenv('VIPERDB_ANALYSIS_PATH')
    subprocess.check_output([os.path.join(path, 'scripts/delete_entry.pl'),'-e %s' % mms_entry.entry_key])

    if virus:
        Layer.objects.filter(entry_id=virus.entry_id).delete()
        Virus.objects.filter(entry_id=virus.entry_id).delete()
        LayerEntity.objects.filter(entry_id=virus.entry_id).delete()


class StepTwoView(FormView):
    template_name = "add_entry/step_two.html"
    form_class = VirusForm

    def get_initial(self):
        initial = super(StepTwoView, self).get_initial()
        initial.update({'entry_id': self.request.session['entry_id']})
        return initial

    def get_context_data(self, **kwargs):
        context = super(StepTwoView, self).get_context_data(**kwargs)
        context.update({'entry_id': self.request.session['entry_id']})
        return context

    def get_success_url(self):
        return reverse('add_entry:step_three')

    def form_valid(self, virus_form):
        entry_id = self.request.session['entry_id']
        virus = virus_form.save(commit=False)
        prepare_virus(virus, entry_id)
        virus.save()

        mms_entry = MmsEntry.objects.get(entry_key=str(virus.entry_key))
        prepare_mms_entry(mms_entry, virus)
        mms_entry.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, virus_form):
        return super(StepTwoView, self).form_invalid(virus_form)


@ajax_request
def start_pdbase(request):
    """Starts PDBase as well as gets the entry_key"""
    if request.method == 'GET':
        entry_id = request.GET['entry_id']
        m = send_task('virus.run_pdbase', args=[entry_id], kwargs={}).get()
        entry_key = MmsEntry.objects.filter(id=entry_id).latest('entry_key')
        return {"pdbase": m, "entry_key": int(str(entry_key))}
    else:
        return {"message": "No entry_id specified!"}

def get_entry_key(entry_id):
    """Take an entry_id and get it's corresponding entry_key"""
    return MmsEntry.objects.filter(id=entry_id).latest('entry_key').entry_key

def prepare_virus(virus, entry_id): 
    """Prepare virus for entry into database"""
    virus.entry_key = get_entry_key(entry_id)
    virus.prepared = False

def prepare_mms_entry(mms_entry, virus):
    """Prepare mms_entry after virus deposition"""
    mms_entry.deposition_date = virus.deposition_date


class StepThreeView(FormView):
    template_name = "add_entry/step_three.html"
    form_class = MatrixChoiceForm
    unit_matrix = [1,0,0,0,
                   0,1,0,0,
                   0,0,1,0]
    input_matrix = []

    def get_viperize_matrix(self, entry_id):
        return send_task('virus.get_matrix', args=[entry_id], kwargs={}).get().split()

    def get_layer_formset(self):
        entry_key = get_entry_key(self.request.session['entry_id'])
        LayerFormset = formset_factory(LayerForm)
        LayerFormset.form = staticmethod(curry(LayerForm, entry_key=entry_key))
        return LayerFormset

    def get_context_data(self, **kwargs):
        virus = Virus.objects.get(entry_id=self.request.session['entry_id'])
        self.viperize_matrix = self.get_viperize_matrix(virus.pk)
        mismatched_chains = get_mismatched_chains(virus.entry_key)

        LayerFormset = self.get_layer_formset()(prefix='layers')
        ChainFormset = formset_factory(ChainForm, extra=len(mismatched_chains))

        chain_formset = ChainFormset(prefix="chains")
        for index, chain_form in enumerate(chain_formset):
            chain_form.chain = mismatched_chains[index]

        kwargs = super(StepThreeView, self).get_context_data(**kwargs)
        kwargs.update({
            'layer_formset': self.get_layer_formset(),
            'entry_id': self.request.session['entry_id'],
            'viperize_matrix': make_2d_matrix(self.viperize_matrix, with_vector=True),
            'unit_matrix': make_2d_matrix(self.unit_matrix, with_vector=True),
            'chain_formset': chain_formset,
            'matrix_form': self.get_form(self.form_class),
        })
        return kwargs

    def post(self, request, *args, **kwargs):
        layer_formset = self.get_layer_formset()(request.POST, prefix="layers")
        matrix_form = self.get_form(self.form_class)
        ChainFormset = formset_factory(ChainForm)
        chain_formset = ChainFormset(request.POST, prefix="chains")

        virus = Virus.objects.get(entry_id=self.request.session['entry_id'])

        self.mismatched_chains = get_mismatched_chains(virus.entry_key)
        self.viperize_matrix = self.get_viperize_matrix(virus.pk)

        if (matrix_form.is_valid() and chain_formset.is_valid() and 
            layer_formset.is_valid()):
            return self.form_valid(request, virus, matrix_form, chain_formset, 
                                   layer_formset)
        else:
            return self.form_invalid(request, virus, matrix_form, chain_formset, 
                                     layer_formset)

    def form_valid(self, request, virus, matrix_form, chain_formset, layer_formset):

        for index, layer_form in enumerate(layer_formset):
            layer = layer_form.save(commit=False)
            prepare_layer(virus, layer)
            layer.save()

            save_layer_entities(virus, layer, layer_form.cleaned_data['entities'])
        virus.layer_count = len(layer_formset)

        # VIPER Matrix Selection
        matrix_choice = int(matrix_form.cleaned_data['matrix_selection'])
        if matrix_choice is Virus.MTX_UNIT:
            user_matrix = unit_matrix
        if matrix_choice is Virus.MTX_INPUT:
            user_matrix = request.POST.getlist('matrix')
        elif matrix_choice is Virus.MTX_VIPERIZE:
            user_matrix = self.viperize_matrix

        matrix = make_2d_matrix(user_matrix)
        vector = [user_matrix[(i*4) + 3] for i in range(3)]
        prepare_matrix(virus, matrix, vector)
        virus.save()

        # This will fail if chains have already been renamed
        for index, chain_form in enumerate(chain_formset):
            chain_choice = int(chain_form.cleaned_data['chain_selection'])
            if chain_choice is Virus.CHAIN_REVERT:
                rename_chain(virus.entry_key, 
                             self.mismatched_chains[index]['label_asym_id'], 
                             self.mismatched_chains[index]['auth_asym_id'])
            elif chain_choice is Virus.CHAIN_INPUT:
                rename_chain(virus.entry_key, 
                             self.mismatched_chains[index]['label_asym_id'], 
                             chain_form.cleaned_data['chain_input'])
            elif chain_choice is Virus.CHAIN_MAINTAIN:
                # Do nothing.
                pass

        send_task('virus.make_vdb', args=[request.session['entry_id']], kwargs={})
        return redirect(reverse('add_entry:step_four'))

    def form_invalid(self, request, virus, matrix_form, chain_formset):
        pass

def prepare_layer(virus, layer):
    """Prepare layer for entry into database"""
    layer.entry_key = virus.entry_key
    layer.entry_id = virus

def save_layer_entities(virus, layer, entities):
    """Saves LayerEntity association table entries"""
    LayerEntity.objects.bulk_create([
        LayerEntity(entry_id=virus, layer_key=layer, entity_key=entity)
        for entity in entities
    ])

def make_2d_matrix(src_matrix, with_vector=False):
    """Turns a 1x12 vector into a 3x4 matrix"""
    return [[src_matrix[(i*4)+j] for j in range(4)] for i in range(3)]

def prepare_matrix(virus, matrix, vector):
    """Prepare virus with given matrix and vector"""
    for i in range(3):
        for j in range(3):
            index = "%s_%s" % (str(i), str(j))
            setattr(virus, 'matrix_%s' % (index), matrix[i][j])
        setattr(virus, 'vector_%s' % (str(i)), vector[i])

def rename_chain(entry_key, chain_to_rename, rename_to):
    # TODO - Finish rename_chain
    atom_sites = (AtomSite.objects.filter(entry_key=entry_key, 
                                          label_asym_id=chain_to_rename)
                                  .update(label_asym_id=rename_to))
    print atom_sites


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

        chains = (AtomSite.objects
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
            for chain in chains:
                au_matrix = move_chain(virus, chain['label_asym_id'], 
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
        pass


def move_chain(virus, chain, matrix_number):
    """Moving chains from one orientation to another"""
    seq_range = AtomSite.objects.filter(entry_key=virus.entry_key, label_asym_id=chain).aggregate(Min('auth_seq_id'), Max('auth_seq_id'))
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

class StepFiveView(TemplateView):
    template_name = "add_entry/step_five.html"

    def get_context_data(self, **kwargs):
        context = super(StepFiveView, self).get_context_data(**kwargs)
        context.update({'entry_id': self.request.session['entry_id']})
        return context
