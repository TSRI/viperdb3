from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from annoying.decorators import ajax_request
from celery.execute import send_task
from annoying.functions import get_object_or_None


from viperdb.forms.add_entry import VirusForm, LayerForm
from viperdb.models import MmsEntry, LayerEntity, Entity, StructRef

class StepTwoView(FormView):
    template_name = "add_entry/step_two.html"
    form_class = VirusForm

    def get_initial(self):
        initial = super(StepTwoView, self).get_initial()
        initial.update({'entry_id': self.request.session['entry_id']})
        return initial

    def get_context_data(self, **kwargs):
        kwargs = super(StepTwoView, self).get_context_data(**kwargs)
        kwargs.update({'layer_formset': formset_factory(LayerForm),
                       'entry_id' : self.request.session['entry_id']})

        return kwargs

    def get_success_url(self):
        return reverse('add_entry:step_three')

    def post(self, request, *args, **kwargs):
        virus_form = self.get_form(self.form_class)
        layer_formset = formset_factory(LayerForm)
        layer_formset = layer_formset(request.POST)

        if virus_form.is_valid() and layer_formset.is_valid():
            return self.form_valid(virus_form, layer_formset)
        else:
            return self.form_invalid(virus_form, layer_formset)

    def form_valid(self, virus_form, layer_formset):
        entry_id = self.request.session['entry_id']
        virus = virus_form.save(commit=False)
        prepare_virus(virus, entry_id, layer_formset)
        virus.save()

        mms_entry = MmsEntry.objects.get(entry_key=str(virus.entry_key))
        prepare_mms_entry(mms_entry, virus)
        mms_entry.save()

        virus_polymers = Entity.objects.filter(type='polymer', entry_key=virus.entry_key)
        entity_choices = self.request.POST.getlist('entity_accession_id')
        for index, layer_form in enumerate(layer_formset):
            layer = layer_form.save(commit=False)
            prepare_layer(virus, layer)
            layer.save()

            entity_selections = self.request.POST.getlist('entity_accession_id_' + str(index))

            layer_entity_dict = {
                'virus': virus,
                'virus_polymers': virus_polymers,
                'layer': layer,
                'entity_choices': entity_choices, 
                'entity_selections': entity_selections,
            }
            for layer_entity in prepare_layer_entities(**layer_entity_dict):
                layer_entity.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, virus_form, layer_formset):
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

@ajax_request
def get_polymers(request, entry_id):
    r = StructRef.objects.filter(entry_id=entry_id)
    return {"polymers": r}

def prepare_virus(virus, entry_id, virus_layers): 
    """Prepare virus for entry into database"""
    virus.entry_key = (MmsEntry.objects.filter(id=virus.entry_id)
                                       .latest('entry_key').entry_key)
    virus.layer_count = len(virus_layers)
    virus.prepared = False

def prepare_mms_entry(mms_entry, virus):
    """Prepare mms_entry after virus deposition"""
    mms_entry.deposition_date = virus.deposition_date

def prepare_layer(virus, layer):
    """Prepare layer for entry into database"""
    layer.entry_key = virus.entry_key
    layer.entry_id = virus

def prepare_layer_entities(virus, virus_polymers, layer, entity_choices, entity_selections):
    """Prepares and yields layer entities"""

    for index, entity_selection in enumerate(virus_polymers):
        if entity_selections[index] == 'on':
            struct_ref = get_object_or_None(StructRef, 
                                            entry_key=virus.entry_key, 
                                            pdbx_db_accession=entity_choices[index])
            if not struct_ref:
                struct_ref = (StructRef.objects
                              .filter(entry_key=virus.entry_key)
                              .order_by('entity_key')[index])
            layer_entity = LayerEntity(entity_key=struct_ref.entity_key, 
                                       layer_key=layer, 
                                       entry_id=virus)
            yield layer_entity