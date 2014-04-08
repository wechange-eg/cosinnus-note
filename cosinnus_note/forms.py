# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from cosinnus.forms.attached_object import FormAttachable
from cosinnus.forms.group import GroupKwargModelFormMixin
from cosinnus.forms.tagged import TagObjectFormMixin

from cosinnus_note.models import Comment, Note


class NoteForm(GroupKwargModelFormMixin, TagObjectFormMixin, FormAttachable):

    class Meta:
        model = Note
        fields = ('title', 'text', 'tags', 'video',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
