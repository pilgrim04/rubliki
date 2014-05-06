# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'rubliki_1_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('birth_date', self.gf('django.db.models.fields.DateField')(default='1900-01-01')),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'rubliki_1', ['User'])

        # Adding model 'Currency'
        db.create_table(u'rubliki_1_currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('currency', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'rubliki_1', ['Currency'])

        # Adding model 'BillingTypes'
        db.create_table(u'rubliki_1_billingtypes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('billing_type', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'rubliki_1', ['BillingTypes'])

        # Adding model 'Billing'
        db.create_table(u'rubliki_1_billing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rubliki_1.User'])),
            ('billing_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('billing_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rubliki_1.BillingTypes'])),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rubliki_1.Currency'])),
            ('money', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'rubliki_1', ['Billing'])

        # Adding model 'CategoryTypes'
        db.create_table(u'rubliki_1_categorytypes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category_type', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'rubliki_1', ['CategoryTypes'])

        # Adding model 'Category'
        db.create_table(u'rubliki_1_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rubliki_1.User'])),
            ('category_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rubliki_1.CategoryTypes'])),
        ))
        db.send_create_signal(u'rubliki_1', ['Category'])

        # Adding model 'Subcategory'
        db.create_table(u'rubliki_1_subcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rubliki_1.Category'])),
            ('subcategory_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'rubliki_1', ['Subcategory'])

        # Adding model 'TransactionType'
        db.create_table(u'rubliki_1_transactiontype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transaction_type', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'rubliki_1', ['TransactionType'])

        # Adding model 'Transaction'
        db.create_table(u'rubliki_1_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rubliki_1.User'])),
            ('billing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rubliki_1.Billing'])),
            ('transaction_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rubliki_1.TransactionType'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rubliki_1.Category'])),
            ('subcategory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rubliki_1.Subcategory'])),
            ('money', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'rubliki_1', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'rubliki_1_user')

        # Deleting model 'Currency'
        db.delete_table(u'rubliki_1_currency')

        # Deleting model 'BillingTypes'
        db.delete_table(u'rubliki_1_billingtypes')

        # Deleting model 'Billing'
        db.delete_table(u'rubliki_1_billing')

        # Deleting model 'CategoryTypes'
        db.delete_table(u'rubliki_1_categorytypes')

        # Deleting model 'Category'
        db.delete_table(u'rubliki_1_category')

        # Deleting model 'Subcategory'
        db.delete_table(u'rubliki_1_subcategory')

        # Deleting model 'TransactionType'
        db.delete_table(u'rubliki_1_transactiontype')

        # Deleting model 'Transaction'
        db.delete_table(u'rubliki_1_transaction')


    models = {
        u'rubliki_1.billing': {
            'Meta': {'object_name': 'Billing'},
            'billing_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'billing_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rubliki_1.BillingTypes']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rubliki_1.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rubliki_1.User']"})
        },
        u'rubliki_1.billingtypes': {
            'Meta': {'object_name': 'BillingTypes'},
            'billing_type': ('django.db.models.fields.SmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'rubliki_1.category': {
            'Meta': {'object_name': 'Category'},
            'category_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'category_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rubliki_1.CategoryTypes']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rubliki_1.User']"})
        },
        u'rubliki_1.categorytypes': {
            'Meta': {'object_name': 'CategoryTypes'},
            'category_type': ('django.db.models.fields.SmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'rubliki_1.currency': {
            'Meta': {'object_name': 'Currency'},
            'currency': ('django.db.models.fields.SmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'rubliki_1.subcategory': {
            'Meta': {'object_name': 'Subcategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rubliki_1.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subcategory_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'rubliki_1.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'billing': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rubliki_1.Billing']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rubliki_1.Category']"}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'subcategory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rubliki_1.Subcategory']"}),
            'transaction_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rubliki_1.TransactionType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rubliki_1.User']"})
        },
        u'rubliki_1.transactiontype': {
            'Meta': {'object_name': 'TransactionType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transaction_type': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        u'rubliki_1.user': {
            'Meta': {'object_name': 'User'},
            'birth_date': ('django.db.models.fields.DateField', [], {'default': "'1900-01-01'"}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        }
    }

    complete_apps = ['rubliki_1']