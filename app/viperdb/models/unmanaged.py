
from django.db import models

class MmsEntry(models.Model):
    class Meta:
        app_label = "viperdb"
        db_table = 'MMS_ENTRY'
        managed = False

    entry_key = models.IntegerField(primary_key=True, db_column='entry_key')
    id = models.ForeignKey("Virus", to_field='entry_id', 
                           related_name='mms_entry', 
                           db_column='id')
    deposition_date = models.DateField()

    def __unicode__(self):
        return str(self.entry_key)

class AtomSite(models.Model):
    class Meta:
        app_label = "viperdb"
        db_table = 'ATOM_SITE'
        managed = False

    atom_site_key = models.IntegerField(primary_key=True)
    entry_key = models.ForeignKey(MmsEntry, to_field='entry_key', related_name='atom_site', db_column='entry_key')
    auth_asym_id = models.CharField(max_length=255, db_column='auth_asym_id')
    auth_seq_id = models.IntegerField(db_column='auth_seq_id')
    label_asym_id = models.CharField(max_length=255, db_column='label_asym_id')
    label_entity_key = models.ForeignKey('Entity', db_column='label_entity_key')

class Entity(models.Model):
    class Meta:
        app_label = "viperdb"
        db_table = 'ENTITY'
        managed = False

    entity_key = models.AutoField(primary_key=True, db_column='entity_key')
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key')
    pdbx_description = models.TextField()
    type = models.CharField(max_length=255)

class StructRef(models.Model):
    class Meta:
        app_label = "viperdb"
        db_table = 'STRUCT_REF'
        managed = False

    struct_ref_key = models.AutoField(primary_key=True, db_column='struct_ref_key')
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key')
    entity_key = models.ForeignKey(Entity, db_column='entity_key')
    pdbx_db_accession = models.CharField(max_length=255)

class IcosMatrix(models.Model):
    class Meta:
        app_label = "viperdb"
        db_table = 'ICOS_MATRIX'
        managed = False

    icos_matrix_key = models.AutoField(primary_key=True, db_column='icos_matrix_key')
    matrix_0_0 = models.FloatField(db_column='matrix_0_0')
    matrix_0_1 = models.FloatField(db_column='matrix_0_1')
    matrix_0_2 = models.FloatField(db_column='matrix_0_2')
    matrix_1_0 = models.FloatField(db_column='matrix_1_0')
    matrix_1_1 = models.FloatField(db_column='matrix_1_1')
    matrix_1_2 = models.FloatField(db_column='matrix_1_2')
    matrix_2_0 = models.FloatField(db_column='matrix_2_0')
    matrix_2_1 = models.FloatField(db_column='matrix_2_1')
    matrix_2_2 = models.FloatField(db_column='matrix_2_2')


class AuMatrix(models.Model):
    class Meta:
        app_label = "viperdb"
        db_table = "AU_MATRIX"
        managed = False

    au_matrix_key = models.IntegerField(primary_key=True)
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key')
    label_entity_key = models.ForeignKey(Entity, db_column='label_entity_key')
    entry_id = models.ForeignKey("Virus", to_field='entry_id', db_column='entry_id')
    label_asym_id = models.CharField(max_length=32, db_column='label_asym_id')
    seq_range_string = models.CharField(max_length=32, db_column='seq_range_string')
    matrix_0_0 = models.FloatField(db_column='matrix_0_0')
    matrix_0_1 = models.FloatField(db_column='matrix_0_1')
    matrix_0_2 = models.FloatField(db_column='matrix_0_2')
    matrix_1_0 = models.FloatField(db_column='matrix_1_0')
    matrix_1_1 = models.FloatField(db_column='matrix_1_1')
    matrix_1_2 = models.FloatField(db_column='matrix_1_2')
    matrix_2_0 = models.FloatField(db_column='matrix_2_0')
    matrix_2_1 = models.FloatField(db_column='matrix_2_1')
    matrix_2_2 = models.FloatField(db_column='matrix_2_2')
    vector_0   = models.FloatField(db_column='vector_0')
    vector_1   = models.FloatField(db_column='vector_1')
    vector_2   = models.FloatField(db_column='vector_2')


class VirusEnergy(models.Model):
    """
        Unmanaged Django model for virus_energy
        Some fields are not completed.
        These are known as 'interfaces'
    """
    class Meta:
        app_label = "viperdb"
        db_table = "VIRUS_ENERGY"
        managed = False

    virus_energy_key = models.IntegerField(primary_key=True)
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key')
    entry_id = models.ForeignKey("Virus", db_column='entry_id', 
                                 related_name='interfaces')
    layer_key = models.ForeignKey("Layer", db_column='layer_key')
    auth_1_asym_id = models.CharField(max_length=255, db_column='auth_1_asym_id')
    auth_2_asym_id = models.CharField(max_length=255, db_column='auth_2_asym_id')
    viper_matrix_1 = models.IntegerField(db_column='viper_matrix_1')
    viper_matrix_2 = models.IntegerField(db_column='viper_matrix_2')
    assocn_nrg_total = models.FloatField(db_column='assocn_nrg_total')
    bsa_total = models.FloatField(db_column='bsa_total')


class Struct(models.Model):
    """
        Unmanaged model for struct_ref
        Some fields are not completed
    """
    class Meta:
        app_label = "viperdb"
        db_table = "STRUCT"
        managed = False

    struct_key = models.AutoField(primary_key=True)
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key')
    entry_id = models.ForeignKey("Virus", db_column='entry_id', related_name='struct')
    title = models.CharField(max_length=255)
    pdbx_descriptor = models.CharField(max_length=255)


class VirusResidueAsaManager(models.Manager):
    def get_query_set(self):
        exclusion = ['ADE', 'URA', 'GUA', 'URI', 
                     "CYT", "THY", "U", "A", 
                     "G", "C", "T"]
        qs = super(VirusResidueAsaManager, self).get_query_set()
        for e in exclusion:
            qs = qs.exclude(label_asym_id=[e])
        return qs


class VirusResidueAsa(models.Model):
    """ Unmanaged model for virus_residue_asa. Some fields are not completed """
    class Meta:
        app_label = "viperdb"
        db_table = "VIRUS_RESIDUE_ASA"
        managed = False

    objects = VirusResidueAsaManager()

    virus_residue_asa_key = models.AutoField(primary_key=True)
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key')
    entry_id = models.ForeignKey("Virus", db_column='entry_id', 
                                 related_name='residue_asa')
    label_asym_id = models.CharField(max_length=255, db_column="label_asym_id")
    label_seq_id = models.IntegerField(db_column="label_seq_id")
    label_comp_id = models.CharField(max_length=255, db_column="label_comp_id")
    radius_aa = models.FloatField(db_column="radius_aa")
    radius_min = models.FloatField(db_column="radius_min")
    sasa_bound = models.FloatField(db_column="sasa_bound")