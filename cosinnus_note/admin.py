# -*- coding: utf-8 -*-
from django.contrib import admin

from embed_video.admin import AdminVideoMixin

from cosinnus_note.models import Note


class NoteModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ('title', 'group', 'creator',)
    list_filter = ('group',)

admin.site.register(Note, NoteModelAdmin)
