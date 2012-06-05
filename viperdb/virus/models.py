from django.db import models

# Create your models here.
from django.db.models.deletion import CASCADE

class Virus (models.Model):
    FILE_REMOTE = 1
    FILE_LOCAL = 2
    FILE_UPLOAD = 3
    FILE_SOURCE_CHOICES = ((FILE_REMOTE, 'Use up-to-date PDB and CIF files from RCSB'),
                           (FILE_LOCAL, 'Use existing PDB and CIF files on VIPERdb'),
                           (FILE_UPLOAD, 'Upload your own PDB and CIF files to VIPERdb'))
    MTX_VIPERIZE = 1
    MTX_INPUT = 2
    MTX_UNIT = 3
    MATRIX_CHOICES = ((MTX_VIPERIZE,'Use viperize to generate PDB to VIPER matrix'),
                      (MTX_INPUT, 'Input your own matrix'),
                      (MTX_UNIT, 'Use Unix Matrix'))

    CHAIN_REVERT = 1
    CHAIN_INPUT = 2
    CHAIN_MAINTAIN = 3
    CHAIN_CHOICES = ((CHAIN_REVERT, 'Change it back.'),
                     (CHAIN_INPUT, 'Provide your own label: '),
                     (CHAIN_MAINTAIN, 'Leave it as is.'))

    def clean(self):
        self.entry_id = self.entry_id.lower()

    def __unicode__(self):
        return self.entry_id

    def get_tnumber(self):
        return self.layers.all()[0].tnumber

    def get_chains(self):
        return VirusResidueAsa.objects.filter(entry_key=self.entry_key).distinct('label_asym_id')

    entry_id = models.CharField(max_length=8, primary_key=True, db_column='entry_id')
    entry_key = models.ForeignKey('MmsEntry', db_column='entry_key', unique=True)
    pubmed_id = models.CharField(max_length=8, blank=True, null=True, verbose_name='Pubmed ID')
    name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255)
    deposition_date = models.DateField()
    genome = models.CharField(max_length=8)
    family = models.CharField(max_length=32, null=True, blank=True)
    genus = models.CharField(max_length=32)
    host = models.CharField(max_length=32)
    resolution = models.FloatField(blank=True, null=True)
    unique = models.BooleanField()
    unique_relative_id = models.ForeignKey('self', null=True, blank=True)
    layer_count = models.IntegerField()
    matrix_0_0 = models.FloatField(editable=False, null=True, blank=True)
    matrix_0_1 = models.FloatField(editable=False, null=True, blank=True)
    matrix_0_2 = models.FloatField(editable=False, null=True, blank=True)
    matrix_1_0 = models.FloatField(editable=False, null=True, blank=True)
    matrix_1_1 = models.FloatField(editable=False, null=True, blank=True)
    matrix_1_2 = models.FloatField(editable=False, null=True, blank=True)
    matrix_2_0 = models.FloatField(editable=False, null=True, blank=True)
    matrix_2_1 = models.FloatField(editable=False, null=True, blank=True)
    matrix_2_2 = models.FloatField(editable=False, null=True, blank=True)
    vector_0 = models.FloatField(editable=False, null=True, blank=True)
    vector_1 = models.FloatField(editable=False, null=True, blank=True)
    vector_2 = models.FloatField(editable=False, null=True, blank=True)
    min_diameter = models.FloatField(editable=False, null=True, blank=True)
    ave_diameter = models.FloatField(editable=False, null=True, blank=True)
    max_diameter = models.FloatField(editable=False, null=True, blank=True)
    prepared = models.BooleanField()
    times_viewed = models.IntegerField(editable=False, default=0, blank=True)
    private = models.BooleanField(editable=False)

class Layer(models.Model):
    layer_key = models.AutoField(primary_key=True)
    layer_id = models.CharField(max_length=32, verbose_name="Layer ID")
    entry_key = models.ForeignKey('MmsEntry', db_column='entry_key', unique=True)
    entry_id = models.ForeignKey(Virus, to_field='entry_id', db_column='entry_id', related_name='layers')
    layer_name = models.CharField(max_length=255)
    tnumber = models.CharField(max_length=5, verbose_name="T-Number")
    subunit_name = models.CharField(max_length=5)
    min_diameter = models.FloatField(editable=False, null=True, blank=True, verbose_name="Minimum Diameter")
    ave_diameter = models.FloatField(editable=False, null=True, blank=True, verbose_name="Average Diameter")
    max_diameter = models.FloatField(editable=False, null=True, blank=True, verbose_name="Maximum Diameter")

class LayerEntity(models.Model):
    layer_key = models.ForeignKey(Layer, primary_key=True, db_column='layer_key')
    entity_key = models.IntegerField()
    entry_key = models.IntegerField()

class MmsEntry(models.Model):
    class Meta:
        db_table = 'mms_entry'
        managed = False

    entry_key = models.IntegerField(primary_key=True, db_column='entry_key')
    id = models.ForeignKey(Virus, to_field='entry_id', related_name='mms_entry', db_column='id')
    deposition_date = models.DateField()

    def __unicode__(self):
        return str(self.entry_key)

class AtomSite(models.Model):
    class Meta:
        db_table = 'atom_site'
        managed = False

    atom_site_key = models.IntegerField(primary_key=True)
    entry_key = models.ForeignKey(MmsEntry, to_field='entry_key', related_name='atom_site', db_column='entry_key')
    auth_asym_id = models.CharField(max_length=255, db_column='auth_asym_id')
    auth_seq_id = models.IntegerField(db_column='auth_seq_id')
    label_asym_id = models.CharField(max_length=255, db_column='label_asym_id')
    label_entity_key = models.ForeignKey('Entity', db_column='label_entity_key')

class Entity(models.Model):
    class Meta:
        db_table = 'entity'
        managed = False

    entity_key = models.AutoField(primary_key=True, db_column='entity_key')
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key')
    pdbx_description = models.TextField()
    type = models.CharField(max_length=255)

class StructRef(models.Model):
    class Meta:
        db_table = 'struct_ref'
        managed = False

    struct_ref_key = models.AutoField(primary_key=True, db_column='struct_ref_key')
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key')
    entity_key = models.ForeignKey(Entity, db_column='entity_key')
    pdbx_db_accession = models.CharField(max_length=255)

class IcosMatrix(models.Model):
    class Meta:
        db_table = 'icos_matrix'
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
        db_table = "au_matrix"
        managed = False

    au_matrix_key = models.IntegerField(primary_key=True)
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key')
    label_entity_key = models.ForeignKey(Entity, db_column='label_entity_key')
    entry_id = models.ForeignKey(Virus, to_field='entry_id', db_column='entry_id')
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
        db_table = "virus_energy"
        managed = False

    virus_energy_key = models.IntegerField(primary_key=True)
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key')
    entry_id = models.ForeignKey(Virus, db_column='entry_id', related_name='interfaces')
    layer_key = models.ForeignKey(Layer, db_column='layer_key')
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
        db_table = "struct"
        managed = False

    struct_key = models.AutoField(primary_key=True)
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key')
    entry_id = models.ForeignKey(Virus, db_column='entry_id', related_name='struct')
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
        db_table = "virus_residue_asa"
        managed = False

    objects = VirusResidueAsaManager()

    virus_residue_asa_key = models.AutoField(primary_key=True)
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key')
    entry_id = models.ForeignKey(Virus, db_column='entry_id', related_name='residue_asa')
    label_asym_id = models.CharField(max_length=255, db_column="label_asym_id")
    label_seq_id = models.IntegerField(db_column="label_seq_id")
    label_comp_id = models.CharField(max_length=255, db_column="label_comp_id")
    radius_aa = models.FloatField(db_column="radius_aa")
    radius_min = models.FloatField(db_column="radius_min")
    sasa_bound = models.FloatField(db_column="sasa_bound")




    
