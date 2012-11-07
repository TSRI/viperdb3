from django.db import models

# Create your models here.
from django.db.models.deletion import CASCADE

class Virus (models.Model):

    class Meta:
        app_label = "viperdb"

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

    def clean_family(self):
        if self.family:
            self.family = self.family.lower()

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
    unique_relative = models.ForeignKey('Virus', null=True, blank=True)
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
    
