# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from cosinnus.forms.attached_object import FormAttachable
from cosinnus.forms.group import GroupKwargModelFormMixin
from cosinnus.forms.tagged import get_form
from cosinnus.forms.user import UserKwargModelFormMixin

from cosinnus_note.models import Comment, Note


class _NoteForm(GroupKwargModelFormMixin, UserKwargModelFormMixin,
                FormAttachable):

    class Meta:
        model = Note
        fields = ('title', 'text', 'tags', 'video',)


#: A django-multiform :class:`MultiModelForm`. Includs support for `group` and
#: `attached_objects_querysets` arguments being passed to the underlying main
#: form (:class:`_NoteForm`)
NoteForm = get_form(_NoteForm)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
