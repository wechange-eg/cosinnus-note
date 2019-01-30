# -*- coding: utf-8 -*-
from django.contrib import admin

from cosinnus_note.models import Note
from cosinnus.admin import BaseTaggableAdminMixin


class NoteModelAdmin(BaseTaggableAdminMixin, admin.ModelAdmin):
    list_display = BaseTaggableAdminMixin.list_display + ['short_text', ]
    search_fields = BaseTaggableAdminMixin.search_fields + ['text', ]
    
admin.site.register(Note, NoteModelAdmin)
