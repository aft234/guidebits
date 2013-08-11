# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Word'
        db.create_table(u'product_word', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('root', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('synonyms', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'product', ['Word'])

        # Adding model 'Search'
        db.create_table(u'product_search', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product.Product'])),
            ('complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('total_results', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'product', ['Search'])

        # Adding model 'Tweet'
        db.create_table(u'product_tweet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('search', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['product.Search'])),
        ))
        db.send_create_signal(u'product', ['Tweet'])


    def backwards(self, orm):
        # Deleting model 'Word'
        db.delete_table(u'product_word')

        # Deleting model 'Search'
        db.delete_table(u'product_search')

        # Deleting model 'Tweet'
        db.delete_table(u'product_tweet')


    models = {
        u'product.product': {
            'Meta': {'ordering': "['created']", 'object_name': 'Product'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'related_names': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.search': {
            'Meta': {'object_name': 'Search'},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Product']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'total_results': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Search']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.word': {
            'Meta': {'object_name': 'Word'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'root': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'synonyms': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['product']