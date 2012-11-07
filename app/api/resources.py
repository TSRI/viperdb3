from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from viperdb.models import Virus, VirusEnergy, Entity, MmsEntry, Struct
from viperdb.models import VirusResidueAsa, AtomSite

class VirusResource(ModelResource):
    interfaces = fields.ToManyField('api.resources.InterfaceResource', 
                                    'interfaces', 
                                    full=True)
    class Meta:
        queryset = Virus.objects.all()
        resource_name = 'virus'
        filtering = {
            'entry_id': ALL,
            'family': ALL_WITH_RELATIONS,
        } 
        list_allowed_methods =['get']
        detail_allowed_methods =['get']

class InterfaceResource(ModelResource):
    # virus = fields.ToOneField('api.resources.VirusResource',
    #                               'entry_id', 
    #                               full=True)
    class Meta:
        queryset = VirusEnergy.objects.all()
        resource_name = 'interface'
        filtering = {
            'virus': ALL_WITH_RELATIONS,
        }


class AtomSiteResource(ModelResource):
    entry_key = fields.ToOneField('api.resources.MmsEntryResource',
                                  'entry_key',
                                  full=True)
    class Meta:
        queryset = AtomSite.objects.distinct('label_asym_id')
        resource_name = 'atom_site'
        filtering = {
            'entry_key': ALL,
        }


class PolymerResource(ModelResource):
    entry_key = fields.ToOneField('api.resources.MmsEntryResource', 
                                  'entry_key',
                                  full=True)
    class Meta:
        queryset = Entity.objects.filter(type='polymer')
        resource_name = 'polymer'
        filtering = {
            'entry_key': ALL,
        }


class MmsEntryResource(ModelResource):
    class Meta:
        queryset = MmsEntry.objects.all()
        resource_name = 'mms_entry'


class StructResource(ModelResource):
    entry_key = fields.ToOneField('api.resources.MmsEntryResource', 'entry_key', full=True)
    class Meta:
        queryset = Struct.objects.all()
        resource_name = 'struct'
        filtering = {
            'entry_key': ALL,
        }


class VirusResidueAsaResource(ModelResource):
    entry_key = fields.ToOneField('api.resources.MmsEntryResource',
                                  'entry_key',
                                  full=True)
    class Meta:
        queryset = VirusResidueAsa.objects.all()
        resource_name = "residue_asa"
        filtering = {
            'entry_key': ALL,
            'entry_id': ALL,
            'label_asym_id': ALL,
        }


