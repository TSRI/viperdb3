from django.db import models
from viperdb.models import Virus, MmsEntry, Entity

class Layer(models.Model):
    layer_key = models.AutoField(primary_key=True)
    layer_id = models.CharField(max_length=32, verbose_name="Layer ID")
    entry_key = models.ForeignKey(MmsEntry, db_column='entry_key', 
                                  unique=True)
    entry_id = models.ForeignKey(Virus, to_field='entry_id', 
                                 db_column='entry_id', related_name='layers')
    layer_name = models.CharField(max_length=255)
    tnumber = models.CharField(max_length=5, verbose_name="T-Number")
    subunit_name = models.CharField(max_length=5)
    min_diameter = models.FloatField(editable=False, null=True, blank=True, 
                                     verbose_name="Minimum Diameter")
    ave_diameter = models.FloatField(editable=False, null=True, blank=True, 
                                     verbose_name="Average Diameter")
    max_diameter = models.FloatField(editable=False, null=True, blank=True, 
                                     verbose_name="Maximum Diameter")


class LayerEntity(models.Model):
    layer_key = models.ForeignKey(Layer, primary_key=True, db_column='layer_key')
    entity_key = models.ForeignKey(Entity)
    entry_key = models.ForeignKey(Virus)

