from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import FormView

from celery.execute import send_task

from viperdb.forms.add_entry import MoveChainForm, ImageAnalysisForm
from viperdb.models import Virus, AtomSite

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
