from django.conf.urls.defaults import *
from tastypie.api import Api
from api.resources import VirusResource, InterfaceResource, PolymerResource
from api.resources import MmsEntryResource, StructResource
from api.resources import VirusResidueAsaResource, AtomSiteResource

virus = VirusResource()
interface = InterfaceResource()
polymer = PolymerResource() 
mms_entry = MmsEntryResource() 
struct = StructResource()
residue_asa = VirusResidueAsaResource()
atom_site = AtomSiteResource()

api = Api(api_name='v1')
api.register(virus, canonical=True)
api.register(interface, canonical=True)
api.register(polymer, canonical=True)
api.register(mms_entry, canonical=True)
api.register(struct, canonical=True)
api.register(residue_asa, canonical=True)
api.register(atom_site, canonical=True)

urlpatterns = patterns('', 
    (r'^v1/', include(virus.urls)),
    (r'^v1/', include(interface.urls)),
    (r'^v1/', include(polymer.urls)),
    (r'^v1/', include(mms_entry.urls)),
    (r'^v1/', include(struct.urls)),
    (r'^v1/', include(residue_asa.urls)),
    (r'^v1/', include(atom_site.urls)),
)

urlpatterns += patterns('viperdb.api.views',
    url(r'^v1/phi_psi/$', 'phi_psi', name='phi_psi'),
)
