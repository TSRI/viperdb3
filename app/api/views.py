from annoying.decorators import ajax_request
from django.shortcuts import get_object_or_404
from django.db import connection, transaction
from django.http import HttpResponse
from viperdb.models import Virus
from viperdb.api.phi_psi import phi_psi_query 
from decimal import Decimal
from math import acos, cos, sin
import json

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return "%.2f" % (obj)
        return json.JSONEncoder.default(self, obj)

def dictfetchall(cursor):
    """ Returns all rows from a cursor as a dict"""
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row)) 
        for row in cursor.fetchall()
    ]

def add_cartesian(residue):
    d_to_r = acos(-1) / 180 #Degrees to radians
    residue['x'] = round((225 * cos(residue['phi']*d_to_r) * sin(residue['psi']*d_to_r) + 256), 2)
    residue['y'] = round(-((440 * sin(residue['phi']*d_to_r) * sin(residue['psi']*d_to_r) - 512) / 2), 2)
    return residue

def phi_psi(request):
    """Custom API method for Phi-Psi Explorer"""
    #TODO add alternative output methods
    if request.method == 'GET':
        entry_key = request.GET.get('entry_key', 4)
        virus = get_object_or_404(Virus, entry_key=4)
        # TODO get all available filtering from url
        virus_dict = {
            "entry_id": virus.entry_id,
            "entry_key": int(str(entry_key)),
            "order_by": request.GET.get('order_by', "RID"),
            "asc_desc": request.GET.get('asc_desc', "ASC"),
            "sic": request.GET.get('sic', "INTERFACE"),
            "limit": int(request.GET.get('limit', 10000)),
            "subunit": request.GET.get('subunit', 'A'), 
            "label_asym_id": request.GET.get('label_asym_id', 'A')
        }

        cursor = connection.cursor()
        cursor.execute(phi_psi_query(virus_dict))
        residues = dictfetchall(cursor)

        residues = map(add_cartesian, residues)
        r_dict = {
            "meta": {"total_count": len(residues)},
            "objects": residues
        }
        return HttpResponse(content=json.dumps(r_dict, cls=DecimalEncoder), mimetype="application/json")
    else:
        # TODO: take care of response when its not a get
        pass


