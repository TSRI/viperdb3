
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.shortcuts import redirect
from django.views.generic import FormView
from django.utils.functional import curry

from celery.execute import send_task

from viperdb.forms.add_entry import MatrixChoiceForm, ChainForm, LayerForm
from viperdb.helpers import get_mismatched_chains
from viperdb.models import Virus, MmsEntry, LayerEntity, AtomSite
from viperdb.views.add_entry.step_two import get_entry_key

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

        layer_formset = self.get_layer_formset()(prefix='layers')
        ChainFormset = formset_factory(ChainForm, extra=len(mismatched_chains))

        chain_formset = ChainFormset(prefix="chains")
        for index, chain_form in enumerate(chain_formset):
            chain_form.chain = mismatched_chains[index]

        kwargs = super(StepThreeView, self).get_context_data(**kwargs)
        kwargs.update({
            'layer_formset': layer_formset,
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

    def form_invalid(self, request, virus, matrix_form, chain_formset, layer_formset):
        return redirect(reverse("add_entry:step_three"))

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

