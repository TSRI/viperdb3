from annoying.decorators import ajax_request
from annoying.functions import get_object_or_None
from celery.execute import send_task

from viperdb.models import MmsEntry, StructRef, LayerEntity, AtomSite, Virus

@ajax_request
def start_pdbase(request):
    """Starts PDBase as well as gets the entry_key"""
    if request.method == 'GET':
        entry_id = request.GET['entry_id']
        m = send_task('virus.run_pdbase', args=[entry_id], kwargs={}).get()
        entry_key = MmsEntry.objects.filter(id=entry_id).latest('entry_key')
        return {"pdbase": m, "entry_key": int(str(entry_key))}
    else:
        return {"message": "No entry_id specified!"}

@ajax_request
def get_polymers(request, entry_id):
    r = StructRef.objects.filter(entry_id=entry_id)
    return {"polymers": r}

def prepare_virus(virus, entry_id, virus_layers): 
    """Prepare virus for entry into database"""
    virus.entry_key = (MmsEntry.objects.filter(id=virus.entry_id)
                                       .latest('entry_key').entry_key)
    virus.layer_count = len(virus_layers)
    virus.prepared = False

def prepare_mms_entry(mms_entry, virus):
    """Prepare mms_entry after virus deposition"""
    mms_entry.deposition_date = virus.deposition_date

def prepare_layer(virus, layer):
    """Prepare layer for entry into database"""
    layer.entry_key = virus.entry_key
    layer.entry_id = virus

def prepare_layer_entities(virus, virus_polymers, layer, entity_choices, entity_selections):
    """Prepares and yields layer entities"""

    for index, entity_selection in enumerate(virus_polymers):
        if entity_selections[index] == 'on':
            struct_ref = get_object_or_None(StructRef, 
                                            entry_key=virus.entry_key, 
                                            pdbx_db_accession=entity_choices[index])
            if not struct_ref:
                struct_ref = (StructRef.objects
                              .filter(entry_key=virus.entry_key)
                              .order_by('entity_key')[index])
            layer_entity = LayerEntity(entity_key=struct_ref.entity_key, 
                                       layer_key=layer, 
                                       entry_id=virus)
            yield layer_entity


def make_2d_matrix(src_matrix, with_vector=False):
    """Turns a 1x12 vector into a 3x4 matrix"""
    return [[src_matrix[(i*4)+j] for j in range(4)] for i in range(3)]

def prepare_matrix(virus, matrix, vector):
    """Prepare virus with given matrix and vector"""
    for i in range(3):
        for j in range(3):
            index = "%s_%s" % (str(i), str(j))
            setattr(virus, 'matrix_%s' % (index), matrix[i][j])
        setattr(virus, 'vector_%s' % (str(i)), vector[i])

def rename_chain(entry_key, chain_to_rename, rename_to):
    # TODO - Finish rename_chain
    atom_sites = AtomSite.objects.filter(entry_key=entry_key, label_asym_id=chain_to_rename).update(label_asym_id=rename_to)
    print atom_sites



def move_chain(virus, chain, matrix_number):
    """Moving chains from one orientation to another"""
    seq_range = AtomSite.objects.filter(entry_key=virus.entry_key, label_asym_id=chain).aggregate(Min('auth_seq_id'), Max('auth_seq_id'))
    icos_matrix = IcosMatrix.objects.get(pk=matrix_number)
    entity_key = AtomSite.objects.filter(label_asym_id=chain, entry_key=virus.entry_key).distinct().order_by('label_asym_id')[0].label_entity_key
    au_matrix = get_object_or_None(AuMatrix, entry_id=virus.entry_id)
    if not au_matrix:
        au_matrix = AuMatrix(au_matrix_key=AuMatrix.objects.count()+1, entry_key=MmsEntry.objects.get(pk=virus.entry_key), entry_id=virus, label_entity_key=entity_key, label_asym_id=chain, seq_range_string=str(seq_range['auth_seq_id__min']) + "-" + str(seq_range['auth_seq_id__max']))

    [[setattr(au_matrix, 'matrix_' + str(i) + '_' + str(j), getattr(icos_matrix, 'matrix_' + str(i) + '_' + str(j))) for j in range(3)] for i in range(3)]
    [[setattr(au_matrix, 'matrix_%s_%s' % (str(i), str(j)), getattr(icos_matrix, 'matrix_%s_%s' % (str(i), str(j)))) for j in range(3)] for i in range(3)]
    [setattr(au_matrix, 'vector_%s' % (str(i)), 0) for i in range(3)]
    return au_matrix

def prepare_diameters(layer, diameters):
    """Prepare layer with diameter information"""
    diameter_types = ["min", "ave", "max"]
    for index, diameter in enumerate(diameters):
        setattr(layer, "%s_diameter" % (diameter_types[index]), diameter)

def get_diameters(virus):
    """Calls script to return diameters"""
    # TODO - Add logic to re-use existing diameters
    return send_task('virus.get_diameters', args=[virus.entry_id], kwargs={}).get()

def save_diameters(virus, diameters):
    """Sets diameters for given virus"""
    # TODO - Add logic for multiple layers    
    for layer in virus.layers.all():
        # diameters = get_diameters(virus)
        # if diameters:
        prepare_diameters(layer, diameters)
        layer.save()