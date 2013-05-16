# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Empresa'
        db.create_table(u'Sistema_Principal_empresa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('nit', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('ciudad', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('imagen', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('correo', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('cuotas_no_aplic', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
        ))
        db.send_create_signal(u'Sistema_Principal', ['Empresa'])

        # Adding model 'Usuario'
        db.create_table(u'Sistema_Principal_usuario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40, db_index=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=254)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('apellidos', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('esta_activo', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('es_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'Sistema_Principal', ['Usuario'])

        # Adding M2M table for field groups on 'Usuario'
        db.create_table(u'Sistema_Principal_usuario_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usuario', models.ForeignKey(orm[u'Sistema_Principal.usuario'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(u'Sistema_Principal_usuario_groups', ['usuario_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Usuario'
        db.create_table(u'Sistema_Principal_usuario_user_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usuario', models.ForeignKey(orm[u'Sistema_Principal.usuario'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(u'Sistema_Principal_usuario_user_permissions', ['usuario_id', 'permission_id'])

        # Adding M2M table for field empresa on 'Usuario'
        db.create_table(u'Sistema_Principal_usuario_empresa', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usuario', models.ForeignKey(orm[u'Sistema_Principal.usuario'], null=False)),
            ('empresa', models.ForeignKey(orm[u'Sistema_Principal.empresa'], null=False))
        ))
        db.create_unique(u'Sistema_Principal_usuario_empresa', ['usuario_id', 'empresa_id'])

        # Adding model 'Cliente'
        db.create_table(u'Sistema_Principal_cliente', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cedula', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('apellidos', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('not_por_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sistema_Principal.Empresa'])),
        ))
        db.send_create_signal(u'Sistema_Principal', ['Cliente'])

        # Adding model 'Kit'
        db.create_table(u'Sistema_Principal_kit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('soat', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('casco', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('chaleco', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('transporte', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('placa', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sistema_Principal.Empresa'])),
        ))
        db.send_create_signal(u'Sistema_Principal', ['Kit'])

        # Adding model 'Matricula'
        db.create_table(u'Sistema_Principal_matricula', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre_ciudad', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('precio', self.gf('django.db.models.fields.IntegerField')(max_length=20)),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sistema_Principal.Empresa'])),
        ))
        db.send_create_signal(u'Sistema_Principal', ['Matricula'])

        # Adding model 'Moto'
        db.create_table(u'Sistema_Principal_moto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre_fabr', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('referencia', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('modelo', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('precio_publico', self.gf('django.db.models.fields.IntegerField')(max_length=14)),
            ('cuota_minima', self.gf('django.db.models.fields.IntegerField')(max_length=15)),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sistema_Principal.Empresa'])),
            ('matricula_asociada', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sistema_Principal.Matricula'])),
            ('kit_asociado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sistema_Principal.Kit'])),
        ))
        db.send_create_signal(u'Sistema_Principal', ['Moto'])

        # Adding model 'Inventario_motos'
        db.create_table(u'Sistema_Principal_inventario_motos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('moto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sistema_Principal.Moto'])),
            ('en_venta', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sistema_Principal.Empresa'])),
        ))
        db.send_create_signal(u'Sistema_Principal', ['Inventario_motos'])

        # Adding model 'T_financiacion'
        db.create_table(u'Sistema_Principal_t_financiacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('num_meses', self.gf('django.db.models.fields.IntegerField')(unique=True, max_length=2)),
            ('valor_por', self.gf('django.db.models.fields.FloatField')()),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sistema_Principal.Empresa'])),
        ))
        db.send_create_signal(u'Sistema_Principal', ['T_financiacion'])

        # Adding model 'Cotizacion'
        db.create_table(u'Sistema_Principal_cotizacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha_cot', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('moto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sistema_Principal.Moto'])),
            ('vendedor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sistema_Principal.Usuario'])),
            ('cliente', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sistema_Principal.Cliente'])),
            ('cuota_inicial', self.gf('django.db.models.fields.IntegerField')()),
            ('empresa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sistema_Principal.Empresa'])),
        ))
        db.send_create_signal(u'Sistema_Principal', ['Cotizacion'])

        # Adding M2M table for field n_cuotas on 'Cotizacion'
        db.create_table(u'Sistema_Principal_cotizacion_n_cuotas', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cotizacion', models.ForeignKey(orm[u'Sistema_Principal.cotizacion'], null=False)),
            ('t_financiacion', models.ForeignKey(orm[u'Sistema_Principal.t_financiacion'], null=False))
        ))
        db.create_unique(u'Sistema_Principal_cotizacion_n_cuotas', ['cotizacion_id', 't_financiacion_id'])


    def backwards(self, orm):
        # Deleting model 'Empresa'
        db.delete_table(u'Sistema_Principal_empresa')

        # Deleting model 'Usuario'
        db.delete_table(u'Sistema_Principal_usuario')

        # Removing M2M table for field groups on 'Usuario'
        db.delete_table('Sistema_Principal_usuario_groups')

        # Removing M2M table for field user_permissions on 'Usuario'
        db.delete_table('Sistema_Principal_usuario_user_permissions')

        # Removing M2M table for field empresa on 'Usuario'
        db.delete_table('Sistema_Principal_usuario_empresa')

        # Deleting model 'Cliente'
        db.delete_table(u'Sistema_Principal_cliente')

        # Deleting model 'Kit'
        db.delete_table(u'Sistema_Principal_kit')

        # Deleting model 'Matricula'
        db.delete_table(u'Sistema_Principal_matricula')

        # Deleting model 'Moto'
        db.delete_table(u'Sistema_Principal_moto')

        # Deleting model 'Inventario_motos'
        db.delete_table(u'Sistema_Principal_inventario_motos')

        # Deleting model 'T_financiacion'
        db.delete_table(u'Sistema_Principal_t_financiacion')

        # Deleting model 'Cotizacion'
        db.delete_table(u'Sistema_Principal_cotizacion')

        # Removing M2M table for field n_cuotas on 'Cotizacion'
        db.delete_table('Sistema_Principal_cotizacion_n_cuotas')


    models = {
        u'Sistema_Principal.cliente': {
            'Meta': {'object_name': 'Cliente'},
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'cedula': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Empresa']"}),
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
            'moto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Moto']"}),
            'n_cuotas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['Sistema_Principal.T_financiacion']", 'symmetrical': 'False'}),
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
            'moto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Moto']"})
        },
        u'Sistema_Principal.kit': {
            'Meta': {'object_name': 'Kit'},
            'casco': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'chaleco': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Empresa']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'placa': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'soat': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'transporte': ('django.db.models.fields.IntegerField', [], {'max_length': '10'})
        },
        u'Sistema_Principal.matricula': {
            'Meta': {'object_name': 'Matricula'},
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Empresa']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre_ciudad': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'precio': ('django.db.models.fields.IntegerField', [], {'max_length': '20'})
        },
        u'Sistema_Principal.moto': {
            'Meta': {'object_name': 'Moto'},
            'cuota_minima': ('django.db.models.fields.IntegerField', [], {'max_length': '15'}),
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Empresa']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kit_asociado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Kit']"}),
            'matricula_asociada': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Matricula']"}),
            'modelo': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'nombre_fabr': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'precio_publico': ('django.db.models.fields.IntegerField', [], {'max_length': '14'}),
            'referencia': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'Sistema_Principal.t_financiacion': {
            'Meta': {'object_name': 'T_financiacion'},
            'empresa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sistema_Principal.Empresa']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_meses': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '2'}),
            'valor_por': ('django.db.models.fields.FloatField', [], {})
        },
        u'Sistema_Principal.usuario': {
            'Meta': {'object_name': 'Usuario'},
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'empresa': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['Sistema_Principal.Empresa']", 'null': 'True', 'blank': 'True'}),
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