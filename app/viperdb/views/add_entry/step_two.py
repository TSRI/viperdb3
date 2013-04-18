from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from viperdb.forms.add_entry import VirusForm, LayerForm
from viperdb.models import MmsEntry, LayerEntity

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
        pass