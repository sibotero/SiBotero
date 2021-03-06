# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Cotizacion.moto'
        db.delete_column(u'Sistema_Principal_cotizacion', 'moto_id')

        # Adding M2M table for field moto on 'Cotizacion'
        db.create_table(u'Sistema_Principal_cotizacion_moto', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cotizacion', models.ForeignKey(orm[u'Sistema_Principal.cotizacion'], null=False)),
            ('moto', models.ForeignKey(orm[u'Sistema_Principal.moto'], null=False))
        ))
        db.create_unique(u'Sistema_Principal_cotizacion_moto', ['cotizacion_id', 'moto_id'])


    def backwards(self, orm):
        # Adding field 'Cotizacion.moto'
        db.add_column(u'Sistema_Principal_cotizacion', 'moto',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['Sistema_Principal.Moto']),
                      keep_default=False)

        # Removing M2M table for field moto on 'Cotizacion'
        db.delete_table('Sistema_Principal_cotizacion_moto')


    models = {
        u'Sistema_Principal.cliente': {
            'Meta': {'object_name': 'Cliente'},
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'cedula': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Empresa']"}),
            'es_vip': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'not_por_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'Sistema_Principal.cotizacion': {
            'Meta': {'object_name': 'Cotizacion'},
            'cliente': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Cliente']"}),
            'cuota_inicial': ('django.db.models.fields.IntegerField', [], {}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Empresa']"}),
            'fecha_cot': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matricula_asociada': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Matricula']"}),
            'medio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Medio_Publicitario']"}),
            'moto': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Sistema_Principal.Moto']", 'symmetrical': 'False'}),
            'n_cuotas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Sistema_Principal.T_financiacion']", 'symmetrical': 'False'}),
            'n_no_aplicables': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'no_aplicables': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vendedor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Usuario']"})
        },
        u'Sistema_Principal.empresa': {
            'Meta': {'object_name': 'Empresa'},
            'ciudad': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'correo': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'cuotas_no_aplic': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'nit': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'Sistema_Principal.inventario_motos': {
            'Meta': {'object_name': 'Inventario_motos'},
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Empresa']"}),
            'en_venta': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Moto']", 'unique': 'True'})
        },
        u'Sistema_Principal.kit': {
            'Meta': {'object_name': 'Kit'},
            'casco': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'chaleco': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Empresa']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moto_asociada': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Moto']"}),
            'placa': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'soat': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'transporte': ('django.db.models.fields.IntegerField', [], {'max_length': '10'})
        },
        u'Sistema_Principal.matricula': {
            'Meta': {'unique_together': "(['nombre_ciudad', 'empresa'],)", 'object_name': 'Matricula'},
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Empresa']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre_ciudad': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'precio': ('django.db.models.fields.IntegerField', [], {'max_length': '20'})
        },
        u'Sistema_Principal.medio_publicitario': {
            'Meta': {'object_name': 'Medio_Publicitario'},
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Empresa']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identificador': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'medio': ('django.db.models.fields.CharField', [], {'max_length': "'30'"})
        },
        u'Sistema_Principal.moto': {
            'Meta': {'unique_together': "(('modelo', 'referencia', 'empresa'),)", 'object_name': 'Moto'},
            'cuota_minima': ('django.db.models.fields.IntegerField', [], {'max_length': '15'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Empresa']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modelo': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'nombre_fabr': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'precio_publico': ('django.db.models.fields.IntegerField', [], {'max_length': '14'}),
            'referencia': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'Sistema_Principal.t_financiacion': {
            'Meta': {'unique_together': "(('num_meses', 'empresa'),)", 'object_name': 'T_financiacion'},
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Empresa']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_meses': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'valor_por': ('django.db.models.fields.FloatField', [], {})
        },
        u'Sistema_Principal.usuario': {
            'Meta': {'object_name': 'Usuario'},
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'ciudad': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'empresa': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Sistema_Principal.Empresa']", 'symmetrical': 'False'}),
            'es_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'esta_activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Sistema_Principal']