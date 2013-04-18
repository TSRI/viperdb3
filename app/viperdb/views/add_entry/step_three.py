
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.shortcuts import redirect
from django.views.generic import FormView

from celery.execute import send_task

from viperdb.forms.add_entry import MatrixChoiceForm, ChainForm
from viperdb.helpers import get_mismatched_chains
from viperdb.models import Virus, MmsEntry, LayerEntity

class StepThreeView(FormView):
    template_name = "add_entry/step_three.html"
    form_class = MatrixChoiceForm
    unit_matrix = [1,0,0,0,
                   0,1,0,0,
                   0,0,1,0]
    input_matrix = []

    def get_viperize_matrix(self, entry_id):
        return send_task('virus.get_matrix', args=[entry_id], kwargs={}).get().split()

    def get_context_data(self, **kwargs):
        virus = Virus.objects.get(entry_id=self.request.session['entry_id'])
        self.viperize_matrix = self.get_viperize_matrix(virus.pk)
        mismatched_chains = get_mismatched_chains(virus.entry_key)
        ChainFormset = formset_factory(ChainForm, extra=len(mismatched_chains))

        chain_formset = ChainFormset()
        for index, chain_form in enumerate(chain_formset):
            chain_form.chain = mismatched_chains[index]

        kwargs = super(StepThreeView, self).get_context_data(**kwargs)
        kwargs.update({
            'viperize_matrix': make_2d_matrix(self.viperize_matrix, with_vector=True),
            'unit_matrix': make_2d_matrix(self.unit_matrix, with_vector=True),
            'chain_formset': chain_formset,
            'matrix_form': self.get_form(self.form_class),
        })
        return kwargs

    def post(self, request, *args, **kwargs):

        matrix_form = self.get_form(self.form_class)
        chain_formset = self.get_form(formset_factory(ChainForm))
        virus = Virus.objects.get(entry_id=self.request.session['entry_id'])

        self.mismatched_chains = get_mismatched_chains(virus.entry_key)
        self.viperize_matrix = self.get_viperize_matrix(virus.pk)

        if matrix_form.is_valid() and chain_formset.is_valid():
            return self.form_valid(request, virus, matrix_form, chain_formset)
        else:
            return self.form_invalid(request, virus, matrix_form, chain_formset)

    def form_valid(self, request, virus, matrix_form, chain_formset):
        matrix_choice = int(matrix_form.cleaned_data['matrix_selection'])

        if matrix_choice is Virus.MTX_UNIT:
            user_matrix = self.unit_matrix
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