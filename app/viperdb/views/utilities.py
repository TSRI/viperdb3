from django.views.generic import ListView, FormView
from django.db.models import Count
from viperdb.forms.search import SearchForm
from viperdb.models import Virus

class GalleryMakerView(ListView):
    model = Virus
    template_name = 'utilities/gallery_maker.html'
    context_object_name = 'viruses'

    def get_context_data(self, **kwargs):
        kwargs = super(GalleryMakerView, self).get_context_data(**kwargs)
        
        families = kwargs['viruses'].values('family').annotate(family_count=Count('family'))
        kwargs.update({'families': families})

        return kwargs



class SearchView(FormView):
    form_class = SearchForm
    template_name = "utilities/search.html"