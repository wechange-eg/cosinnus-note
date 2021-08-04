# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from builtins import object
from cosinnus.views import group
from django.conf import settings
from django import forms
from django.utils.translation import ugettext_lazy as _

from cosinnus.forms.attached_object import FormAttachableMixin
from cosinnus.forms.group import GroupKwargModelFormMixin
from cosinnus.forms.tagged import get_form, BaseTaggableObjectForm
from cosinnus.forms.user import UserKwargModelFormMixin

from cosinnus.models.group import CosinnusPortal
from cosinnus_note.models import Comment, Note


class _NoteForm(GroupKwargModelFormMixin, UserKwargModelFormMixin,
                FormAttachableMixin, BaseTaggableObjectForm):
    
    # HTML required attribute disabled because of the model-required but form-optional field 'title'
    use_required_attribute = False 
    
    class Meta(object):
        model = Note
        fields = ('title', 'text', 'video',)

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(_NoteForm, self).__init__(*args, **kwargs)
        if 'title' in self.initial and self.initial['title'] == Note.EMPTY_TITLE_PLACEHOLDER:
            self.initial['title'] = ''
        if self.fields['title'].initial == Note.EMPTY_TITLE_PLACEHOLDER:
            self.fields['title'].initial = ''

    def group_is_forum(self):
        return self.instance.group.slug == settings.NEWW_FORUM_GROUP_SLUG

    def user_needs_email_validation(self):
        user = self.request.user
        portal = CosinnusPortal.get_current()
        user_email_verified = user.cosinnus_profile.email_verified
        verification_needed = portal.email_needs_verification
        if user.is_authenticated:
            return not user_email_verified and verification_needed

    def check_user_can_not_post(self):
        return self.group_is_forum() and self.user_needs_email_validation()

    def clean(self):
        """ Insert a placeholder title if no title is given """
        title = self.cleaned_data.get('title', None)
        if not title:
            note_text = self.cleaned_data.get('text', None)
            if note_text:
                self.cleaned_data.update({'title': Note.EMPTY_TITLE_PLACEHOLDER},)
                self.errors.pop('title', None)
        if hasattr(self, 'request'):
            if self.check_user_can_not_post():
                raise forms.ValidationError(_('You can not post '
                                              'to this group '
                                              'as long as your '
                                              'email address is '
                                              'not validated.'))
        return super(_NoteForm, self).clean()


#: A django-multiform :class:`MultiModelForm`. Includs support for `group` and
#: `attached_objects_querysets` arguments being passed to the underlying main
#: form (:class:`_NoteForm`)
NoteForm = get_form(_NoteForm)


class CommentForm(forms.ModelForm):

    class Meta(object):
        model = Comment
        fields = ('text',)
