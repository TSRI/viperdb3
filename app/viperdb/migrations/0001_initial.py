# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Virus'
        db.create_table('viperdb_virus', (
            ('entry_id', self.gf('django.db.models.fields.CharField')(max_length=8, primary_key=True, db_column='entry_id')),
            ('entry_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viperdb.MmsEntry'], unique=True, db_column='entry_key')),
            ('pubmed_id', self.gf('django.db.models.fields.CharField')(max_length=8, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('generic_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('deposition_date', self.gf('django.db.models.fields.DateField')()),
            ('genome', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('family', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('genus', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('resolution', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('unique', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('unique_relative', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viperdb.Virus'], null=True, blank=True)),
            ('layer_count', self.gf('django.db.models.fields.IntegerField')()),
            ('matrix_0_0', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('matrix_0_1', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('matrix_0_2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('matrix_1_0', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('matrix_1_1', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('matrix_1_2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('matrix_2_0', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('matrix_2_1', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('matrix_2_2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('vector_0', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('vector_1', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('vector_2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('min_diameter', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('ave_diameter', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('max_diameter', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('prepared', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('times_viewed', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('viperdb', ['Virus'])

        # Adding model 'Layer'
        db.create_table('viperdb_layer', (
            ('layer_key', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('layer_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('entry_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viperdb.MmsEntry'], unique=True, db_column='entry_key')),
            ('entry_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='layers', db_column='entry_id', to=orm['viperdb.Virus'])),
            ('layer_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('tnumber', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('subunit_name', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('min_diameter', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('ave_diameter', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('max_diameter', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('viperdb', ['Layer'])

        # Adding model 'LayerEntity'
        db.create_table('viperdb_layerentity', (
            ('layer_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viperdb.Layer'], primary_key=True, db_column='layer_key')),
            ('entity_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viperdb.Entity'])),
            ('entry_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viperdb.Virus'])),
        ))
        db.send_create_signal('viperdb', ['LayerEntity'])


    def backwards(self, orm):
        # Deleting model 'Virus'
        db.delete_table('viperdb_virus')

        # Deleting model 'Layer'
        db.delete_table('viperdb_layer')

        # Deleting model 'LayerEntity'
        db.delete_table('viperdb_layerentity')


    models = {
        'viperdb.atomsite': {
            'Meta': {'object_name': 'AtomSite', 'db_table': "'ATOM_SITE'", 'managed': 'False'},
            'atom_site_key': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'auth_asym_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'auth_asym_id'"}),
            'auth_seq_id': ('django.db.models.fields.IntegerField', [], {'db_column': "'auth_seq_id'"}),
            'entry_key': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'atom_site'", 'db_column': "'entry_key'", 'to': "orm['viperdb.MmsEntry']"}),
            'label_asym_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'label_asym_id'"}),
            'label_entity_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.Entity']", 'db_column': "'label_entity_key'"})
        },
        'viperdb.aumatrix': {
            'Meta': {'object_name': 'AuMatrix', 'db_table': "'AU_MATRIX'", 'managed': 'False'},
            'au_matrix_key': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'entry_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.Virus']", 'db_column': "'entry_id'"}),
            'entry_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.MmsEntry']", 'db_column': "'entry_key'"}),
            'label_asym_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_column': "'label_asym_id'"}),
            'label_entity_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.Entity']", 'db_column': "'label_entity_key'"}),
            'matrix_0_0': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_0_0'"}),
            'matrix_0_1': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_0_1'"}),
            'matrix_0_2': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_0_2'"}),
            'matrix_1_0': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_1_0'"}),
            'matrix_1_1': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_1_1'"}),
            'matrix_1_2': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_1_2'"}),
            'matrix_2_0': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_2_0'"}),
            'matrix_2_1': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_2_1'"}),
            'matrix_2_2': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_2_2'"}),
            'seq_range_string': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_column': "'seq_range_string'"}),
            'vector_0': ('django.db.models.fields.FloatField', [], {'db_column': "'vector_0'"}),
            'vector_1': ('django.db.models.fields.FloatField', [], {'db_column': "'vector_1'"}),
            'vector_2': ('django.db.models.fields.FloatField', [], {'db_column': "'vector_2'"})
        },
        'viperdb.entity': {
            'Meta': {'object_name': 'Entity', 'db_table': "'ENTITY'", 'managed': 'False'},
            'entity_key': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'entity_key'"}),
            'entry_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.MmsEntry']", 'db_column': "'entry_key'"}),
            'pdbx_description': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'viperdb.icosmatrix': {
            'Meta': {'object_name': 'IcosMatrix', 'db_table': "'ICOS_MATRIX'", 'managed': 'False'},
            'icos_matrix_key': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'icos_matrix_key'"}),
            'matrix_0_0': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_0_0'"}),
            'matrix_0_1': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_0_1'"}),
            'matrix_0_2': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_0_2'"}),
            'matrix_1_0': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_1_0'"}),
            'matrix_1_1': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_1_1'"}),
            'matrix_1_2': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_1_2'"}),
            'matrix_2_0': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_2_0'"}),
            'matrix_2_1': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_2_1'"}),
            'matrix_2_2': ('django.db.models.fields.FloatField', [], {'db_column': "'matrix_2_2'"})
        },
        'viperdb.layer': {
            'Meta': {'object_name': 'Layer'},
            'ave_diameter': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'entry_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'layers'", 'db_column': "'entry_id'", 'to': "orm['viperdb.Virus']"}),
            'entry_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.MmsEntry']", 'unique': 'True', 'db_column': "'entry_key'"}),
            'layer_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'layer_key': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layer_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'max_diameter': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'min_diameter': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'subunit_name': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'tnumber': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'viperdb.layerentity': {
            'Meta': {'object_name': 'LayerEntity'},
            'entity_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.Entity']"}),
            'entry_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.Virus']"}),
            'layer_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.Layer']", 'primary_key': 'True', 'db_column': "'layer_key'"})
        },
        'viperdb.mmsentry': {
            'Meta': {'object_name': 'MmsEntry', 'db_table': "'MMS_ENTRY'", 'managed': 'False'},
            'deposition_date': ('django.db.models.fields.DateField', [], {}),
            'entry_key': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'entry_key'"}),
            'id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mms_entry'", 'db_column': "'id'", 'to': "orm['viperdb.Virus']"})
        },
        'viperdb.struct': {
            'Meta': {'object_name': 'Struct', 'db_table': "'STRUCT'", 'managed': 'False'},
            'entry_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'struct'", 'db_column': "'entry_id'", 'to': "orm['viperdb.Virus']"}),
            'entry_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.MmsEntry']", 'db_column': "'entry_key'"}),
            'pdbx_descriptor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'struct_key': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'viperdb.structref': {
            'Meta': {'object_name': 'StructRef', 'db_table': "'STRUCT_REF'", 'managed': 'False'},
            'entity_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.Entity']", 'db_column': "'entity_key'"}),
            'entry_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.MmsEntry']", 'db_column': "'entry_key'"}),
            'pdbx_db_accession': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'struct_ref_key': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'struct_ref_key'"})
        },
        'viperdb.virus': {
            'Meta': {'object_name': 'Virus'},
            'ave_diameter': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'deposition_date': ('django.db.models.fields.DateField', [], {}),
            'entry_id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'primary_key': 'True', 'db_column': "'entry_id'"}),
            'entry_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.MmsEntry']", 'unique': 'True', 'db_column': "'entry_key'"}),
            'family': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'generic_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'genome': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'layer_count': ('django.db.models.fields.IntegerField', [], {}),
            'matrix_0_0': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'matrix_0_1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'matrix_0_2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'matrix_1_0': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'matrix_1_1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'matrix_1_2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'matrix_2_0': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'matrix_2_1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'matrix_2_2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'max_diameter': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'min_diameter': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prepared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pubmed_id': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'resolution': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'times_viewed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'unique': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unique_relative': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.Virus']", 'null': 'True', 'blank': 'True'}),
            'vector_0': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vector_1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'vector_2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'viperdb.virusenergy': {
            'Meta': {'object_name': 'VirusEnergy', 'db_table': "'VIRUS_ENERGY'", 'managed': 'False'},
            'assocn_nrg_total': ('django.db.models.fields.FloatField', [], {'db_column': "'assocn_nrg_total'"}),
            'auth_1_asym_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'auth_1_asym_id'"}),
            'auth_2_asym_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'auth_2_asym_id'"}),
            'bsa_total': ('django.db.models.fields.FloatField', [], {'db_column': "'bsa_total'"}),
            'entry_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interfaces'", 'db_column': "'entry_id'", 'to': "orm['viperdb.Virus']"}),
            'entry_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.MmsEntry']", 'db_column': "'entry_key'"}),
            'layer_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.Layer']", 'db_column': "'layer_key'"}),
            'viper_matrix_1': ('django.db.models.fields.IntegerField', [], {'db_column': "'viper_matrix_1'"}),
            'viper_matrix_2': ('django.db.models.fields.IntegerField', [], {'db_column': "'viper_matrix_2'"}),
            'virus_energy_key': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'viperdb.virusresidueasa': {
            'Meta': {'object_name': 'VirusResidueAsa', 'db_table': "'VIRUS_RESIDUE_ASA'", 'managed': 'False'},
            'entry_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'residue_asa'", 'db_column': "'entry_id'", 'to': "orm['viperdb.Virus']"}),
            'entry_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['viperdb.MmsEntry']", 'db_column': "'entry_key'"}),
            'label_asym_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'label_asym_id'"}),
            'label_comp_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'label_comp_id'"}),
            'label_seq_id': ('django.db.models.fields.IntegerField', [], {'db_column': "'label_seq_id'"}),
            'radius_aa': ('django.db.models.fields.FloatField', [], {'db_column': "'radius_aa'"}),
            'radius_min': ('django.db.models.fields.FloatField', [], {'db_column': "'radius_min'"}),
            'sasa_bound': ('django.db.models.fields.FloatField', [], {'db_column': "'sasa_bound'"}),
            'virus_residue_asa_key': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['viperdb']