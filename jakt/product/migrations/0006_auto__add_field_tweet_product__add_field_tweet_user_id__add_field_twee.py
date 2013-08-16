# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Tweet.product'
        db.add_column(u'product_tweet', 'product',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['product.Product']),
                      keep_default=False)

        # Adding field 'Tweet.user_id'
        db.add_column(u'product_tweet', 'user_id',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'Tweet.tweet_id'
        db.add_column(u'product_tweet', 'tweet_id',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'Tweet.created_at'
        db.add_column(u'product_tweet', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now()),
                      keep_default=False)

        # Adding field 'Tweet.raw'
        db.add_column(u'product_tweet', 'raw',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


        # Changing field 'Tweet.text'
        db.alter_column(u'product_tweet', 'text', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Product.image'
        db.alter_column(u'product_product', 'image', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):
        # Deleting field 'Tweet.product'
        db.delete_column(u'product_tweet', 'product_id')

        # Deleting field 'Tweet.user_id'
        db.delete_column(u'product_tweet', 'user_id')

        # Deleting field 'Tweet.tweet_id'
        db.delete_column(u'product_tweet', 'tweet_id')

        # Deleting field 'Tweet.created_at'
        db.delete_column(u'product_tweet', 'created_at')

        # Deleting field 'Tweet.raw'
        db.delete_column(u'product_tweet', 'raw')


        # Changing field 'Tweet.text'
        db.alter_column(u'product_tweet', 'text', self.gf('django.db.models.fields.TextField')(null=True))

        # User chose to not deal with backwards NULL issues for 'Product.image'
        raise RuntimeError("Cannot reverse this migration. 'Product.image' and its values cannot be restored.")

    models = {
        u'product.product': {
            'Meta': {'ordering': "['created']", 'object_name': 'Product'},
            'buy_link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'related_names': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'search_cache': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'product.search': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Search'},
            'blob_results': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Product']"}),
            'raw': ('django.db.models.fields.TextField', [], {}),
            'search': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['product.Search']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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