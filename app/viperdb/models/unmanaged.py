
from django.db import models
from viperdb.models.mixins import MatrixMixin

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

    def delete(self, *args, **kwargs):
        from viperdb.models import LayerEntity, Virus
        if Virus.objects.filter(entry_key=self.entry_key).exists():
            LayerEntity.objects.filter(entry_id=self.id).delete()
            self.id.delete()
        super(MmsEntry, self).delete(*args, **kwargs)

class AtomSite(models.Model):
    class Meta:
        app_label = "viperdb"
        db_table = 'ATOM_SITE'
        managed = False

    id = models.AutoField(primary_key=True, db_column='id')
    atom_site_key = models.IntegerField(primary_key=True)
    entry_key = models.ForeignKey(MmsEntry, to_field='entry_key', related_name='atom_site', db_column='entry_key')
    auth_asym_id = models.CharField(max_length=255, db_column='auth_asym_id')
    auth_atom_id = models.CharField(max_length=255, db_column='auth_atom_id')
    auth_comp_id = models.CharField(max_length=255, db_column='auth_comp_id')
    auth_seq_id = models.IntegerField(db_column='auth_seq_id')
    label_asym_id = models.CharField(max_length=255, db_column='label_asym_id')
    label_entity_key = models.ForeignKey('Entity', db_column='label_entity_key')
    cartn_x = models.FloatField(db_column='cartn_x')
    cartn_y = models.FloatField(db_column='cartn_y')
    cartn_z = models.FloatField(db_column='cartn_z')
    occupancy = models.FloatField(db_column='occupancy')
    b_iso_or_equiv = models.FloatField(db_column='b_iso_or_equiv')

    def __unicode__(self):
        return str(self.__dict__)

    def get_2d_matrix(self):
        return [[getattr(self, 'cartn_%s' % x)] for x in ['x','y','z']]

class Entity(models.Model):
    class Meta:
        app_label = "viperdb"
        db_table = 'ENTITY'
        managed = False

    entity_key = models.AutoField(primary_key=True, db_column='entity_key')
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key')
    pdbx_description = models.TextField()
    type = models.CharField(max_length=255, db_column='type')

    def __unicode__(self):
        return self.pdbx_description

class StructRef(models.Model):
    class Meta:
        app_label = "viperdb"
        db_table = 'STRUCT_REF'
        managed = False

    struct_ref_key = models.AutoField(primary_key=True, db_column='struct_ref_key')
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key')
    entity_key = models.ForeignKey(Entity, db_column='entity_key')
    pdbx_db_accession = models.CharField(max_length=255)


class IcosMatrix(models.Model, MatrixMixin):
    class Meta:
        app_label = "viperdb"
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
    vector_0 = models.FloatField(db_column='vector_0')
    vector_1 = models.FloatField(db_column='vector_1')
    vector_2 = models.FloatField(db_column='vector_2')


class AuMatrix(models.Model):
    class Meta:
        app_label = "viperdb"
        db_table = "au_matrix"
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
        db_table = "virus_energy"
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
    solvn_nrg_total = models.FloatField(db_column='solvn_nrg_total')
    interface_type = models.CharField(max_length=255, db_column='interface_type')
    symmetry = models.IntegerField(db_column='symmetry')

    def __unicode__(self):
        return ("%(auth_1_asym_id)s%(viper_matrix_1)s" +
               "-%(auth_2_asym_id)s%(viper_matrix_2)s") % self.__dict__

    def get_symmetry(self):
        return "%(interface_type)s-%(symmetry)s" % self.__dict__


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
        db_table = "virus_residue_asa"
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

    def __unicode__(self):
        return "%s%s" % (self.label_asym_id, self.label_seq_id)

class Qscore(models.Model):
    """ Unmanaged model for qscore. Some fields are not completed """
    class Meta:
        app_label = "viperdb"
        db_table = "qscore"
        managed = False

    qscore_key = models.AutoField(primary_key=True)
    entry_id = models.ForeignKey("Virus", db_column="entry_id", related_name='qscores')
    face_1_asym_id_1 = models.CharField(max_length=255, db_column='face_1_asym_id_1')
    face_1_asym_id_2 = models.CharField(max_length=255, db_column='face_1_asym_id_2')
    face_1_matrix_1  = models.IntegerField(db_column='face_1_matrix_1')
    face_1_matrix_2  = models.IntegerField(db_column='face_1_matrix_2')
    face_1_type = models.CharField(max_length=10, db_column='face_1_type')
    face_1_symm = models.IntegerField(db_column='face_1_symm')
    face_2_asym_id_1 = models.CharField(max_length=255, db_column='face_2_asym_id_1')
    face_2_asym_id_2 = models.CharField(max_length=255, db_column='face_2_asym_id_2')
    face_2_matrix_1  = models.IntegerField(db_column='face_2_matrix_1')
    face_2_matrix_2  = models.IntegerField(db_column='face_2_matrix_2')
    face_2_type = models.CharField(max_length=10, db_column='face_2_type')
    face_2_symm = models.IntegerField(db_column='face_2_symm')
    shared = models.IntegerField(db_column='shared')
    numcon_1 = models.IntegerField(db_column='numcon_1')
    numcon_2 = models.IntegerField(db_column='numcon_2')
    qscore = models.IntegerField(db_column='qscore')

    def get_interface_repr(self):
        inter_str = "%(asym)s%(matrix)s"

        inter_1 = inter_str % {'asym': self.face_1_asym_id_1, "matrix": self.face_1_matrix_1}
        inter_2 = inter_str % {'asym': self.face_1_asym_id_2, "matrix": self.face_1_matrix_2}
        repr1 = "%s-%s" % (inter_1, inter_2)

        inter_1 = inter_str % {'asym': self.face_2_asym_id_1, "matrix": self.face_2_matrix_1}
        inter_2 = inter_str % {'asym': self.face_2_asym_id_2, "matrix": self.face_2_matrix_2}
        repr2 = "%s-%s" % (inter_1, inter_2)

        return "%s:%s" % (repr1, repr2)

    def get_type_repr(self):
        return "%(face_1_type)s-%(face_1_symm)s:%(face_2_type)s-%(face_2_symm)s" % self.__dict__






