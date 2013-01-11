import urllib2
from amara import bindery
from django.db.models.aggregates import Min, Max
from django.shortcuts import get_object_or_404
from viperdb.models import Virus, AtomSite, IcosMatrix, AuMatrix, MmsEntry
from celery.execute import send_task
from annoying.functions import get_object_or_None

# Gets virus information from RCSB
def get_pdb_info(entry_id):
    pdb_url = 'http://www.rcsb.org/pdb/rest/describePDB?structureId=' +entry_id 
    mol_url = 'http://www.rcsb.org/pdb/rest/describeMol?structureId=' +entry_id 

    try:
        req = urllib2.Request(pdb_url)
        pdb_xml = urllib2.urlopen(req).read()
        pdb_info = bindery.parse(pdb_xml)
        pdb_info = pdb_info.PDBdescription.PDB
        entry = {'entry_id': entry_id,
                 'name': pdb_info.title,
                 'pubmed_id': pdb_info.pubmedId,
                 'deposition_date': pdb_info.revision_date,
                 'resolution': pdb_info.resolution,
                 'method': pdb_info.expMethod }

        req = urllib2.Request(mol_url)
        mol_xml = urllib2.urlopen(req).read()
        mol_info = bindery.parse(mol_xml)
        mol_info = mol_info.molDescription.structureId
        polymers = [] 
        accession_ids = []
        for polymer in mol_info.polymer:
            polymer_description = {
                'entity_number': polymer.entityNr,
                'description': polymer.polymerDescription.description
            }
            if polymer.macroMolecule is not None:
                polymer_description['macroMolecule_name'] = polymer.macroMolecule.name
                polymer_description['pdbx_db_accession'] = polymer.macroMolecule.accession.id
                if polymer.macroMolecule.accession.id not in accession_ids:
                    accession_ids.append(polymer.macroMolecule.accession.id)
                    polymers.append(polymer_description)
        entry['polymers'] = polymers
        return entry

    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, pdb_url
    except urllib2.URLError, e:
        print "URL Error:", e.reason, pdb_url



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






