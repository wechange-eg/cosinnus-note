# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Note'
        db.create_table(u'note_note', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notes', on_delete=models.PROTECT, to=orm['auth.User'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=145)),
            ('text', self.gf('markupfield.fields.MarkupField')(rendered_field=True)),
            ('text_markup_type', self.gf('django.db.models.fields.CharField')(default=None, max_length=30)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('_text_rendered', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'note', ['Note'])

        # Adding unique constraint on 'Note', fields ['group', 'slug']
        db.create_unique(u'note_note', ['group_id', 'slug'])

        # Adding model 'Comment'
        db.create_table(u'note_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], on_delete=models.PROTECT)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('note', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['note.Note'])),
            ('text', self.gf('markupfield.fields.MarkupField')(rendered_field=True)),
            ('text_markup_type', self.gf('django.db.models.fields.CharField')(default=None, max_length=30)),
            ('_text_rendered', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'note', ['Comment'])


    def backwards(self, orm):
        # Removing unique constraint on 'Note', fields ['group', 'slug']
        db.delete_unique(u'note_note', ['group_id', 'slug'])

        # Deleting model 'Note'
        db.delete_table(u'note_note')

        # Deleting model 'Comment'
        db.delete_table(u'note_comment')


    models = {
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'note.comment': {
            'Meta': {'ordering': "['created_on']", 'object_name': 'Comment'},
            '_text_rendered': ('django.db.models.fields.TextField', [], {}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'on_delete': 'models.PROTECT'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': u"orm['note.Note']"}),
            'text': ('markupfield.fields.MarkupField', [], {'rendered_field': 'True'}),
            'text_markup_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30'})
        },
        u'note.note': {
            'Meta': {'ordering': "['-created_on', 'title']", 'unique_together': "(('group', 'slug'),)", 'object_name': 'Note'},
            '_text_rendered': ('django.db.models.fields.TextField', [], {}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notes'", 'on_delete': 'models.PROTECT', 'to': u"orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '145'}),
            'text': ('markupfield.fields.MarkupField', [], {'rendered_field': 'True'}),
            'text_markup_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '30'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['note']