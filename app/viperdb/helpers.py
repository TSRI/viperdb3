import urllib2, time
from amara import bindery
from django.db.models.aggregates import Min, Max
from django.shortcuts import get_object_or_404
from viperdb.models import Virus, AtomSite, IcosMatrix, AuMatrix, MmsEntry
from celery.execute import send_task
from annoying.functions import get_object_or_None

import requests

def get_mismatched_chains(entry_key):
    mismatched_chains = []

    chains = (AtomSite.objects
              .values('auth_asym_id', 'label_asym_id', 'label_entity_key__pdbx_description')
              .filter(label_entity_key__entry_key=entry_key)
              .distinct())
    for chain in chains:
        if chain['auth_asym_id'] != chain['label_asym_id']:
            mismatched_chains.append(chain)

    return mismatched_chains

def get_pdb_info(entry_id):
  #returns false if does not exist or a dictionary of

    pdb_url = 'http://www.rcsb.org/pdb/rest/describePDB?structureId=' +entry_id 
    r = requests.get(pdb_url)
    pdb_info = bindery.parse(r.text)
    pdb_info = pdb_info.PDBdescription

    if (len(pdb_info.xml_children) == 0):
      return False

    deposition_date = time.strptime(pdb_info.PDB.deposition_date, "%Y-%m-%d")
    deposition_date = time.strftime("%m-%d-%Y", deposition_date)

    pdb_data = {
      "entry_id": entry_id,
      "pubmed_id": pdb_info.PDB.pubmedId,
      "name": pdb_info.PDB.title,
      "deposition_date": deposition_date,
      "resolution": pdb_info.PDB.resolution,
    }

    return pdb_data






