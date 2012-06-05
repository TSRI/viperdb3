from annoying.decorators import render_to, ajax_request
from viperdb.virus.models import Virus

@render_to("family/index.html")
def index(request):
    """ Homepage for all families, displays all the families in a list """
    families = Virus.objects.values('family').distinct()
    return {"families": families}

@render_to("family/info.html")
def info(request, family_name):
    """ Specific homepage for families """
    viruses = Virus.objects.filter(family=family_name)
    return {"viruses": viruses, "family_name": family_name}

@render_to("family/graph.html")
def graph(request, family_name):
    viruses = Virus.objects.filter(family=family_name)
    return {"viruses": viruses, "family_name": family_name}
