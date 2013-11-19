# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms.models import ModelForm

from cosinnus_note.models import Comment, Note


class NoteForm(ModelForm):

    class Meta:
        model = Note
        fields = ('title', 'text', 'tags',)
        


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text', )
