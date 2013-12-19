# -*- coding: utf-8 -*-
from django.contrib import admin

from cosinnus_note.models import Note
from embed_video.admin import AdminVideoMixin

class NoteModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(Note, NoteModelAdmin)