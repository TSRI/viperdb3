from datetime import datetime
from django.db import models
from django.db.models.deletion import CASCADE

from celery.execute import send_task

from viperdb.models import VirusResidueAsa, VirusEnergy


class Family(models.Model):
    class Meta: 
        app_label = "viperdb"
        verbose_name_plural = 'Families'
        
    name = models.CharField(max_length=32, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Virus (models.Model):
    class Meta:
        app_label = "viperdb"
        verbose_name_plural = 'Viruses'

    MTX_VIPERIZE = 1
    MTX_INPUT = 2
    MTX_UNIT = 3
    MATRIX_CHOICES = ((MTX_VIPERIZE,'Use viperize to generate PDB to VIPER matrix'),
                      (MTX_INPUT, 'Input your own matrix'),
                      (MTX_UNIT, 'Use Unix Matrix'))

    CHAIN_REVERT = 1
    CHAIN_MAINTAIN = 2
    CHAIN_INPUT = 3

    CHAIN_CHOICES = ((CHAIN_REVERT, 'Change it back.'),
                     (CHAIN_MAINTAIN, 'Leave it as is.'),
                     (CHAIN_INPUT, 'Provide your own label:'))

    entry_id = models.CharField(max_length=8, primary_key=True, db_column='entry_id', blank=False)
    entry_key = models.IntegerField(unique=True, editable=False, default="")
    pubmed_id = models.CharField(max_length=8, blank=True, null=True, verbose_name='Pubmed ID', default="")
    name = models.CharField(max_length=255, null=True, blank=True, default="")
    generic_name = models.CharField(max_length=255, null=True, blank=True, default="")
    deposition_date = models.DateField(null=True, blank=True, default=datetime.now)
    genome = models.CharField(max_length=8, null=True, blank=True, default="")
    family = models.ForeignKey(Family, null=True, blank=True)
    genus = models.CharField(max_length=32, null=True, blank=True, default="")
    host = models.CharField(max_length=32, null=True, blank=True, default="")
    resolution = models.FloatField(blank=True, null=True)
    unique = models.BooleanField(default=True)
    unique_relative = models.ForeignKey('Virus', null=True, blank=True)
    layer_count = models.IntegerField(default=1)
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
    prepared = models.BooleanField(default=False)
    times_viewed = models.IntegerField(editable=False, default=0, blank=True)
    private = models.BooleanField(editable=False)

    image_types = {
        #'cages':[],
        #'capsids':[],
        #'capsomers':[],
        'chimera': ['3A.jpg','5A.jpg','8A.jpg','inside.jpg','ribbon.jpg'],
        #'unit': [],
    }

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
        queryset = VirusResidueAsa.objects.filter(entry_key=self.entry_key)
        queryset.query.group_by = ['label_asym_id']
        return queryset

    def get_interfaces(self):
        interfaces = (VirusEnergy.objects.filter(entry_key=self.entry_key)
                .order_by('assocn_nrg_total'))

        interface = max(interfaces, key=lambda x: 'assocn_nrg_total')
        max_association_energy = interface.assocn_nrg_total
        for interface in interfaces:
            percent = (interface.assocn_nrg_total / max_association_energy) * 100
            interface.relative_strength = "%.0f%%" % percent

        return interfaces

    def get_qscores(self):
        qscores = (self.qscores.filter(qscore__gt=0.09, qscore__lt=1.0)
                                .exclude(face_1_symm=0, face_2_symm=0)
                                .order_by('-shared'))
        return qscores

    def analyze(self):
        send_task('virus.start_analysis', args=[self.entry_id])

    def generate_images(self):
        send_task('virus.prepare_images', args=[self.entry_id], kwargs={})
