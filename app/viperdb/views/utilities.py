from django.views.generic import ListView
from django.db.models import Count

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