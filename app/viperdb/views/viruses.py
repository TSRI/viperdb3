
from datetime import datetime

from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, ListView

from annoying.decorators import render_to, ajax_request
from annoying.functions import get_object_or_None
from celery.execute import send_task
from celery.task.sets import subtask
from celery.task.control import revoke, inspect
from viperdb.helpers import get_pdb_info

from viperdb.helpers import get_mismatched_chains 
from viperdb.models import Virus, MmsEntry, LayerEntity, StructRef
from viperdb.models import VirusResidueAsa, Layer, AtomSite, Entity
from viperdb.forms.add_entry import (VirusForm, InitialVirusForm, LayerForm,
                           MatrixChoiceForm, ChainForm, MoveChainForm, 
                           ImageAnalysisForm)

class VirusListView(ListView):
    model = Virus
    template_name = 'virus/index.html'
    context_object_name = 'viruses'

class VirusInfoView(DetailView):
    pk_url_kwarg = 'entry_id'
    context_object_name = 'virus'
    model = Virus
    template_name = 'virus/info.html'

    def get_context_data(self, **kwargs):
        context = super(VirusInfoView, self).get_context_data(**kwargs)
        virus = self.get_object()

        chains = virus.get_chains()
        interfaces = virus.get_interfaces()
        qscores = virus.get_qscores()

        context.update({
            'chains': chains, 
            'interfaces': interfaces, 
            'qscores': qscores
        })
        return context

@render_to("virus/phi_psi.html")
def phi_psi(request, entry_id):
    virus = get_object_or_404(Virus, entry_id=entry_id)
    residue_types = [{'label_comp_id': u'ALL'}]
    residue_types += VirusResidueAsa.objects.distinct().values('label_comp_id').order_by('label_comp_id')
    return {"virus": virus, "residue_types": residue_types}

