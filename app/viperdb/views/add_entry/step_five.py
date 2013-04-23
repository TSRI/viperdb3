from django.views.generic import TemplateView

class StepFiveView(TemplateView):
    template_name = "add_entry/step_five.html"

    def get_context_data(self, **kwargs):
        context = super(StepFiveView, self).get_context_data(**kwargs)
        context.update({'entry_id': self.request.session['entry_id']})
        return context