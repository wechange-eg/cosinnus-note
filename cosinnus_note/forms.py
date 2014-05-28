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
        
    def clean(self):
        """ Insert the first couple of characters from the text if no title is given """
        title = self.cleaned_data.get('title', None)
        if not title:
            note_text = self.cleaned_data.get('text', None)
            if note_text:
                self.cleaned_data.update({'title': note_text[:20]},)
                self.errors.pop('title', None)
        return super(_NoteForm, self).clean()


#: A django-multiform :class:`MultiModelForm`. Includs support for `group` and
#: `attached_objects_querysets` arguments being passed to the underlying main
#: form (:class:`_NoteForm`)
NoteForm = get_form(_NoteForm)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
