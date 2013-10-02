# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms.models import ModelForm

from cosinnus.utils.forms import BootstrapTagWidget

from cosinnus_note.models import Comment, Note


class NoteForm(ModelForm):

    class Meta:
        model = Note
        fields = ('title', 'text', 'text_markup_type', 'tags',)
        widgets = {
            'tags': BootstrapTagWidget(),
        }


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('text', 'text_markup_type',)
