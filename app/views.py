import os
from annoying.decorators import render_to
from viperdb.virus.models import Virus

def project(*args):
    return os.path.join(os.path.dirname(__file__), *args)

@render_to("index.html")
def home(request):
    viruses = Virus.objects.order_by('deposition_date').reverse()[:10]

    return {"viruses": viruses}