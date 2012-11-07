
from annoying.decorators import render_to

from viperdb.models import Virus

@render_to("index.html")
def home(request):
    viruses = Virus.objects.order_by('deposition_date').reverse()[:10]

    return {"viruses": viruses}