import os, subprocess

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from annoying.functions import get_object_or_None
from celery.execute import send_task

from viperdb.forms.add_entry import InitialVirusForm
from viperdb.models import Virus, MmsEntry, Layer, LayerEntity

class StepOneView(FormView):
    template_name = "add_entry/step_one.html"
    form_class = InitialVirusForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StepOneView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('add_entry:step_two')

    def form_valid(self, form):
        entry_id = form.cleaned_data['entry_id']

        virus = get_object_or_None(MmsEntry, id=entry_id)
        if virus:
            path = os.getenv('VIPERDB_ANALYSIS_PATH')
            subprocess.check_output([os.path.join(path, 'scripts/delete_entry.pl'),'-e %s' % virus.entry_key])
            Layer.objects.filter(entry_id=entry_id).delete()
            Virus.objects.filter(entry_id=entry_id).delete()
            LayerEntity.objects.filter(entry_id=entry_id).delete()

        pdb_file_source = int(form.cleaned_data["file_source"])
        if pdb_file_source == InitialVirusForm.FILE_REMOTE:
            send_task("virus.get_pdb_files", args=[entry_id]).get()
                      # kwargs={'callback': subtask('virus.run_pdbase')})
        elif pdb_file_source == InitialVirusForm.FILE_LOCAL:
            task = send_task('virus.check_file_count', args=[entry_id], 
                             kwargs={})
            if task.get() is not 2:
                return redirect(reverse('add_entry:step_one'))
            else:
                send_task('virus.run_pdbase', args=[entry_id], kwargs={})
        elif pdb_file_source == InitialVirusForm.FILE_UPLOAD:
            # TODO: allow for file upload
            # pass
            task = send_task('virus.check_file_count', args=[entry_id], kwargs={})
            if not task.get():
                pdb_file = request.FILES['pdb_file_upload']
                cif_file = request.FILES['cif_file_upload']
                if pdb_file and cif_file:
                    send_task('virus:handle_pdb_files', args=[entry_id, pdb_file, cif_file], kwargs={})
                else:
                    return redirect(reverse('virus:initial_virus'))
            else:
               return redirect(reverse('virus:initial_virus'))
               
        send_task('virus.run_pdbase', args=[entry_id], kwargs={})
        # TODO: options to forgo analysis.

        self.request.session['entry_id'] = entry_id

        return super(StepOneView, self).form_valid(form)

