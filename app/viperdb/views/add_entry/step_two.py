from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from annoying.decorators import ajax_request
from celery.execute import send_task
from annoying.functions import get_object_or_None


from viperdb.forms.add_entry import VirusForm
from viperdb.models import MmsEntry, LayerEntity, Entity, StructRef
from viperdb.helpers import get_pdb_info

class StepTwoView(FormView):
    template_name = "add_entry/step_two.html"
    form_class = VirusForm

    def get_initial(self):
        pdb_info = get_pdb_info(self.request.session['entry_id'])

        initial = super(StepTwoView, self).get_initial()
        initial.update(pdb_info)
        
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
        import pdb; pdb.set_trace()
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
