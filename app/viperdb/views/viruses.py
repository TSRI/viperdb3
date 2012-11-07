
from datetime import datetime

from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, get_object_or_404

from annoying.decorators import render_to, ajax_request
from annoying.functions import get_object_or_None
from celery.execute import send_task
from celery.task.sets import subtask
from celery.task.control import revoke, inspect
from viperdb.helpers import get_pdb_info

from viperdb.helpers import get_mismatched_chains 
from viperdb.models import Virus, MmsEntry, LayerEntity, StructRef
from viperdb.models import VirusResidueAsa, Layer, AtomSite, Entity
from viperdb.forms import (VirusForm, InitialVirusForm, LayerForm,
                           MatrixChoiceForm, ChainForm, MoveChainForm, 
                           ImageAnalysisForm)

@render_to("virus/index.html")
def index(request):
    viruses = Virus.objects.all()
    return {"viruses": viruses}

@render_to("virus/info.html")
def info(request, entry_id):
    virus = get_object_or_404(Virus, entry_id=entry_id)
    chains = virus.get_chains()
    return {"virus": virus, "chains": chains}

@render_to("virus/phi_psi.html")
def phi_psi(request, entry_id):
    virus = get_object_or_404(Virus, entry_id=entry_id)
    residue_types = [{'label_comp_id': u'ALL'}]
    residue_types += VirusResidueAsa.objects.distinct().values('label_comp_id').order_by('label_comp_id')
    return {"virus": virus, "residue_types": residue_types}

