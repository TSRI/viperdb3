from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory

from annoying.decorators import render_to, ajax_request
from annoying.functions import get_object_or_None
from celery.execute import send_task
from celery.task.sets import subtask

from viperdb.forms import (InitialVirusForm, LayerForm, VirusForm)
from viperdb.models import (MmsEntry, Virus)

class StepOneView(FormView):
    template_name = "virus/step_one.html"
    form_class = InitialVirusForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StepOneView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('virus:step_two', args=[self.entry_id])

    def form_valid(self, form):
        self.entry_id = form.cleaned_data['entry_id']

        virus = get_object_or_None(MmsEntry, id=self.entry_id)
        if virus:
            virus.delete()

        pdb_file_source = int(form.cleaned_data["file_source"])
        if pdb_file_source == InitialVirusForm.FILE_REMOTE:
            send_task("virus.get_pdb_files", args=[self.entry_id], 
                      kwargs={'callback': subtask('virus.run_pdbase')})
        elif pdb_file_source == InitialVirusForm.FILE_LOCAL:
            task = send_task('virus.check_file_count', args=[self.entry_id], 
                             kwargs={})
            if task.get() is not 2:
                return redirect(reverse('virus:add_entry'))
            # else:
            #     send_task('virus.run_pdbase', args=[self.entry_id], kwargs={})
        elif pdb_file_source == InitialVirusForm.FILE_UPLOAD:
            # TODO: allow for file upload
            pass
#                task = send_task('virus.check_file_count', args=[self.entry_id], kwargs={})
#                if not task.get():
#                    pdb_file = request.FILES['pdb_file_upload']
#                    cif_file = request.FILES['cif_file_upload']
#                    if pdb_file and cif_file:
#                        send_task('virus:handle_pdb_files', args=[self.entry_id, pdb_file, cif_file], kwargs={})
#                    else:
#                        return redirect(reverse('virus:initial_virus'))
#                else:
#                    return redirect(reverse('virus:initial_virus'))
        # send_task('virus.run_pdbase', args=[self.entry_id], kwargs={})
        # TODO: options to forgo analysis.

        return super(StepOneView, self).form_valid(form)

class StepTwoView(FormView):
    template_name = "virus/step_two.html"
    form_class = VirusForm

    def get_initial(self):
        return {'entry_id': self.kwargs['entry_id']}

    def get_context_data(self, **kwargs):
        kwargs = super(StepTwoView, self).get_context_data(**kwargs)
        kwargs.update({'layer_formset': formset_factory(LayerForm)})

        return kwargs

    def get_success_url(self):
        return reverse('virus:step_three', args=[entry_id])

    def post(self, request, *args, **kwargs):
        virus_form = self.get_form(self.form_class)
        layer_formset = self.get_form(formset_factory(LayerForm))

        if virus_form.is_valid() and layer_formset.is_valid():
            return self.form_valid(virus_form, layer_formset)
        else:
            return self.form_invalid(virus_form, layer_formset)

    def form_valid(virus_form, layer_formset):
        virus = virus_form.save(commit=False)
        prepare_virus(virus, entry_id, layer_formset)
        virus.save()

        mms_entry = MmsEntry.objects.get(entry_key=str(virus.entry_key))
        prepare_mms_entry(mms_entry, virus)
        mms_entry.save()

        virus_polymers = Entity.objects.filter(type='polymer', entry_key=virus.entry_key)
        entity_choices = request.POST.getlist('entity_accession_id')
        for index, layer_form in enumerate(layer_formset):
            layer = layer_form.save(commit=False)
            prepare_layer(virus, layer)
            layer.save()

            entity_selections = request.POST.getlist('entity_accession_id_' + str(index))
            map(lambda l_e: l_e.save(), prepare_layer_entity(virus, virus_polymers, layer, entity_choices, entity_selections))

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(virus_form, layer_formset):
        pass



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

@ajax_request
def get_polymers(request, entry_id):
    r = StructRef.objects.filter(entry_id=entry_id)
    return {"polymers": r}

# @render_to("virus/step_two.html")
# def step_two(request, entry_id):
#     """Step two of virus entry"""
#     LayerFormSet = formset_factory(LayerForm)

#     if request.method == "POST":
#         virus_form = VirusForm(request.POST)
#         layer_formset = LayerFormSet(request.POST)

#         if virus_form.is_valid() and layer_formset.is_valid():
#             virus = virus_form.save(commit=False)
#             prepare_virus(virus, entry_id, layer_formset)
#             virus.save()

#             mms_entry = MmsEntry.objects.get(entry_key=str(virus.entry_key))
#             prepare_mms_entry(mms_entry, virus)
#             mms_entry.save()

#             virus_polymers = Entity.objects.filter(type='polymer', entry_key=virus.entry_key)
#             entity_choices = request.POST.getlist('entity_accession_id')
#             for index, layer_form in enumerate(layer_formset):
#                 layer = layer_form.save(commit=False)
#                 prepare_layer(virus, layer)
#                 layer.save()

#                 entity_selections = request.POST.getlist('entity_accession_id_' + str(index))
#                 map(lambda l_e: l_e.save(), prepare_layer_entity(virus, virus_polymers, layer, entity_choices, entity_selections))
#             return redirect(reverse('virus:step_three', args=[entry_id]))

#     else:
#         layer_formset = LayerFormSet()
#         virus_form = VirusForm(initial={"entry_id": entry_id})

#     return {'form': virus_form, 'layer_formset': layer_formset}

def prepare_virus(virus, entry_id, virus_layers): 
    """Prepare virus for entry into database"""
    virus.entry_key = MmsEntry.objects.filter(id=virus.entry_id).latest('entry_key')
    virus.layer_count = len(virus_layers)
    virus.prepared = False

def prepare_mms_entry(mms_entry, virus):
    """Prepare mms_entry after virus deposition"""
    mms_entry.deposition_date = virus.deposition_date

def prepare_layer(virus, layer):
    """Prepare layer for entry into database"""
    layer.entry_key = virus.entry_key
    layer.entry_id = virus

def prepare_layer_entity(virus, virus_polymers, layer, entity_choices, entity_selections):
    """Prepares and yields layer entities"""
    print len(virus_polymers)
    for index, entity_selection in enumerate(virus_polymers):
        if entity_selections[index] == 'on':
            struct_ref = get_object_or_None(StructRef, 
                                            entry_key=virus.entry_key, 
                                            pdbx_db_accession=entity_choices[index])
            if not struct_ref:
                struct_ref = StructRef.objects.filter(entry_key=virus.entry_key).order_by('entity_key')[index]
            layer_entity = LayerEntity(entity_key=struct_ref.entity_key.pk, 
                                       layer_key=layer, 
                                       entry_key=str(virus.entry_key))
            yield layer_entity


@render_to('virus/step_three.html')
def step_three(request, entry_id):
    """Step three for virus entry"""
    virus = get_object_or_404(Virus, entry_id=entry_id)
    entry_key = virus.entry_key
    unit_matrix = [1,0,0,0,0,1,0,0,0,0,1,0]
    viperize_matrix = send_task('virus.get_matrix', args=[entry_id], kwargs={}).get().split()
    input_matrix = []
    mismatched_chains = get_mismatched_chains(entry_key)

    ChainFormSet = formset_factory(ChainForm, extra=len(mismatched_chains))

    if request.method == "POST":
        matrix_form = MatrixChoiceForm(request.POST)
        chain_formset = ChainFormSet(request.POST)

        if matrix_form.is_valid() and chain_formset.is_valid():
            matrix_choice = int(matrix_form.cleaned_data['matrix_selection'])

            if matrix_choice is Virus.MTX_UNIT:
                input_matrix = unit_matrix
            if matrix_choice is Virus.MTX_INPUT:
                input_matrix = request.POST.getlist('matrix')
            elif matrix_choice is Virus.MTX_VIPERIZE:
                input_matrix = viperize_matrix

            matrix = make_2d_matrix(input_matrix)
            vector = [input_matrix[(i*4) + 3] for i in range(3)]
            prepare_matrix(virus, matrix, vector)
            virus.save()

            for index, chain_form in enumerate(chain_formset):
                chain_choice = int(chain_form.cleaned_data['chain_selection'])
                if chain_choice is Virus.CHAIN_REVERT:
                    rename_chain(entry_key, mismatched_chains[index]['label_asym_id'], mismatched_chains[index]['auth_asym_id'])
                elif chain_choice is Virus.CHAIN_INPUT:
                    rename_chain(entry_key, mismatched_chains[index]['label_asym_id'], chain_form.cleaned_data['chain_input'])
                elif chain_choice is Virus.CHAIN_MAINTAIN:
                    # Do nothing.
                    pass

            send_task('virus.make_vdb', args=[entry_id], kwargs={})
            return redirect(reverse('virus:step_four', args=[entry_id]))
    else:
        matrix_form = MatrixChoiceForm()
        chain_formset = ChainFormSet()
        for index, chain_form in enumerate(chain_formset):
            chain_form.chain = mismatched_chains[index]

    return {"matrix_form": matrix_form,
            "viperize_matrix": make_2d_matrix(viperize_matrix, with_vector=True),
            "unit_matrix": make_2d_matrix(unit_matrix, with_vector=True),
            "chain_formset": chain_formset}

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
    atom_sites = AtomSite.objects.filter(entry_key=entry_key, label_asym_id=chain_to_rename).update(label_asym_id=rename_to)
    print atom_sites

#VDB created at this point.
@render_to('virus/step_four.html')
def step_four(request, entry_id):
    virus = Virus.objects.get(pk=entry_id)
    diameters = get_diameters(virus)

    if request.method == 'POST': 
        chains = AtomSite.objects.filter(entry_key=virus.entry_key).values('label_asym_id').distinct()
        form = MoveChainForm(request.POST)
        ia_form = ImageAnalysisForm(request.POST)

        if form.is_valid() and ia_form.is_valid():
            if int(form.cleaned_data['move_selection']) == MoveChainForm.MOVE_ALL:
                for chain in chains:
                    au_matrix = move_chain(virus, chain['label_asym_id'], int(form.cleaned_data['matrix_selection']))
                    au_matrix.save()
                send_task('virus.make_vdb', args=[entry_id], kwargs={})
                return redirect(reverse("virus:step_four", args=[entry_id]))
            else:
                save_diameters(virus, diameters)

                ia_choice = int(ia_form.cleaned_data['analysis_selection'])
                if ia_choice == ImageAnalysisForm.IMAGE_ONLY:
                    send_task('virus.prepare_images', args=[entry_id], kwargs={})
                elif ia_choice == ImageAnalysisForm.ANALYSIS_ONLY:
                    send_task('virus.start_analysis', args=[entry_id], kwargs= {})
                elif ia_choice == ImageAnalysisForm.BOTH_IMAGE_AND_ANALYSIS:
                    send_task('virus.start_analysis', args=[entry_id], kwargs= {})
                    send_task('virus.prepare_images', args=[entry_id], kwargs={})

                return redirect(reverse("virus:step_five", args=[entry_id]))
    else:
        form = MoveChainForm()
        ia_form = ImageAnalysisForm()

    return {"form": form, "ia_form": ia_form, "diameters": diameters}

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


@render_to('virus/step_five.html')
def step_five(request, entry_id):
    return {"entry_id": entry_id}