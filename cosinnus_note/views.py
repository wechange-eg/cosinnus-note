# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from cosinnus.views.attached_object import (CreateViewAttachable,
    UpdateViewAttachable)

from cosinnus.views.mixins.group import (RequireReadMixin, RequireWriteMixin,
    FilterGroupMixin, GroupFormKwargsMixin, DipatchGroupURLMixin)
from cosinnus.views.mixins.user import UserFormKwargsMixin

from cosinnus_note.forms import CommentForm, NoteForm
from cosinnus_note.models import Note, Comment
from django.contrib import messages
from cosinnus.views.mixins.filters import CosinnusFilterMixin
from cosinnus_note.filters import NoteFilter
from cosinnus_note import cosinnus_notifications
from cosinnus.utils.urls import group_aware_reverse, safe_redirect
from cosinnus.utils.pagination import PaginationTemplateMixin
from cosinnus.views.facebook_integration import FacebookIntegrationViewMixin
from django.utils.encoding import force_text
from cosinnus.models.tagged import BaseTagObject


class NoteCreateView(FacebookIntegrationViewMixin, RequireWriteMixin, FilterGroupMixin, 
                     GroupFormKwargsMixin, UserFormKwargsMixin, CreateViewAttachable):

    form_class = NoteForm
    model = Note
    template_name = 'cosinnus_note/note_form.html'
    form_view = 'add'
    
    message_success = _('Your news post was added successfully.')
    
    def get_context_data(self, **kwargs):
        context = super(NoteCreateView, self).get_context_data(**kwargs)
        context.update({
            'form_view': self.form_view,
        })
        return context
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        ret = super(NoteCreateView, self).form_valid(form)
        
        message_success_addition = ''
        # check if the user wants to post this note to facebook
        if form.data.get('facebook_integration_post_to_timeline', None):
            facebook_success = super(NoteCreateView, self).post_to_facebook(self.request.user.cosinnus_profile, self.object.text, urls=self.object.urls)
            if facebook_success is not None:
                if facebook_success:
                    # save facebook id if not empty to mark this note as shared to facebook
                    self.object.facebook_post_id = facebook_success
                    self.object.save()
                message_success_addition += ' ' + force_text(_('Your news post was also posted on your Facebook timeline.'))
            else:
                messages.warning(self.request, _('We could not post this news post on your Facebook timeline. If this problem persists, please make sure you have granted us all required Facebook permissions, or try disconnecting and re-connecting your Facebook account!'))
        
        # check if the user wants to post this note to the group's facebook fan-page/group
        group = self.group
        if form.data.get('facebook_integration_post_to_group_page', None) and group.facebook_group_id:
            facebook_success = super(NoteCreateView, self).post_to_facebook(self.request.user.cosinnus_profile, 
                                    self.object.text, urls=self.object.urls, fb_post_target_id=group.facebook_group_id)
            if facebook_success is not None:
                if facebook_success:
                    # don't mark anything. we don't care if this was posted to the gorup
                    pass
                    #self.object.facebook_post_id = facebook_success
                    #self.object.save()
                message_success_addition += ' ' + force_text(_('Your news post was also posted on the Facebook Group/Fan-Page.'))
            else:
                messages.warning(self.request, _('We could not post this news post on your Facebook Group/Fan-Page. If this problem persists, please try disconnecting and re-connecting your Facebook account or contacting this project/group\'s administrator!'))
        
        messages.success(self.request, force_text(self.message_success) + message_success_addition)
        return ret
        
    def form_invalid(self, form):
        """
        If the form is invalid, we simply redirect to the success url, except if we come from the create view.
        """
        return super(NoteCreateView, self).form_invalid(form)

    def post(self, request, *args, **kwargs):
        self.referer = self.request.GET.get('next', request.META.get('HTTP_REFERER', group_aware_reverse('cosinnus:note:list', kwargs={'group':self.group})))
        return super(NoteCreateView, self).post(request, *args, **kwargs)
    
    def get_success_url(self):
        # self.referer is set in post() method
        return safe_redirect(self.referer, self.request)

note_create = NoteCreateView.as_view()


class NoteDeleteView(RequireWriteMixin, FilterGroupMixin, DeleteView):

    model = Note
    template_name_suffix = '_delete'
    
    message_success = _('Your news post was deleted successfully.')
    
    def post(self, request, *args, **kwargs):
        self.referer = request.META.get('HTTP_REFERER', group_aware_reverse('cosinnus:note:list', kwargs={'group':self.group}))
        return super(NoteDeleteView, self).post(request, *args, **kwargs)
    
    def get_success_url(self):
        # self.referer is set in post() method
        messages.success(self.request, self.message_success)
        return self.referer

note_delete = NoteDeleteView.as_view()


class NoteDetailView(RequireReadMixin, FilterGroupMixin, DetailView):

    model = Note
    template_name = 'cosinnus_note/note_detail.html'

note_detail = NoteDetailView.as_view()


class NoteIndexView(RequireReadMixin, RedirectView):

    def get_redirect_url(self, **kwargs):
        return group_aware_reverse('cosinnus:note:list', kwargs={'group': self.group})

note_index = NoteIndexView.as_view()


class NoteListView(RequireReadMixin, FilterGroupMixin, CosinnusFilterMixin, 
                   PaginationTemplateMixin, ListView):
    model = Note
    filterset_class = NoteFilter
    per_page = 10
    
    def get_queryset(self, **kwargs):
        qs = super(NoteListView, self).get_queryset()
        qs = qs.prefetch_related('comments__creator__cosinnus_profile', 'attached_objects')
        return qs
    
    def get_context_data(self, **kwargs):
        kwargs.update({
            'form':  NoteForm(group=self.group)
        })
        return super(NoteListView, self).get_context_data(**kwargs)

note_list = NoteListView.as_view()


class NoteEmbedView(DipatchGroupURLMixin, FilterGroupMixin, PaginationTemplateMixin, ListView):
    model = Note
    per_page = 10
    template_name = 'cosinnus_note/note_embed.html'
    
    def get_queryset(self, **kwargs):
        """ Only ever show public notes """
        qs = super(NoteEmbedView, self).get_queryset()
        qs = qs.filter(media_tag__visibility=BaseTagObject.VISIBILITY_ALL).prefetch_related('comments__creator__cosinnus_profile', 'attached_objects')
        return qs
    
note_embed = NoteEmbedView.as_view()


class NoteEmbedGlobalView(PaginationTemplateMixin, ListView):
    """ Displays all notes in this Portal in an embeddable view, not just from a specific group """
    
    model = Note
    per_page = 10
    template_name = 'cosinnus_note/note_embed.html'
    
    def get_queryset(self, **kwargs):
        """ Only ever show public notes """
        qs = Note.objects.all()
        qs = qs.filter(media_tag__visibility=BaseTagObject.VISIBILITY_ALL).prefetch_related('comments__creator__cosinnus_profile', 'attached_objects')
        return qs
    
note_embed_global = NoteEmbedGlobalView.as_view()


class NoteUpdateView(RequireWriteMixin, FilterGroupMixin, GroupFormKwargsMixin,
                     UserFormKwargsMixin, UpdateViewAttachable):

    form_class = NoteForm
    model = Note
    template_name = 'cosinnus_note/note_form.html'
    form_view = 'edit'
    
    message_success = _('Your news post was edited successfully.')
    
    def get_context_data(self, **kwargs):
        context = super(NoteUpdateView, self).get_context_data(**kwargs)
        context.update({
            'form_view': self.form_view,
        })
        return context

    def form_valid(self, form):
        messages.success(self.request, self.message_success)
        return super(NoteUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        return group_aware_reverse('cosinnus:note:list', kwargs={'group': self.group})

note_update = NoteUpdateView.as_view()


class CommentCreateView(RequireWriteMixin, FilterGroupMixin, CreateView):

    form_class = CommentForm
    group_field = 'note__group'
    model = Comment
    template_name = 'cosinnus_note/note_detail.html'
    
    message_success = _('Your comment was added successfully.')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.note = self.note
        messages.success(self.request, self.message_success)
        return super(CommentCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        # always overwrite object here, because we actually display the note as object, 
        # and not the comment in whose view we are in when form_invalid comes back
        context.update({
            'note': self.note,
            'object': self.note, 
        })
        return context

    def get(self, request, *args, **kwargs):
        self.note = get_object_or_404(Note, group=self.group, slug=self.kwargs.get('note_slug'))
        return super(CommentCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.note = get_object_or_404(Note, group=self.group, slug=self.kwargs.get('note_slug'))
        self.referer = request.META.get('HTTP_REFERER', self.note.group.get_absolute_url())
        return super(CommentCreateView, self).post(request, *args, **kwargs)
    
    def get_success_url(self):
        # self.referer is set in post() method
        return self.referer

comment_create = CommentCreateView.as_view()


class CommentDeleteView(RequireWriteMixin, FilterGroupMixin, DeleteView):

    group_field = 'note__group'
    model = Comment
    template_name_suffix = '_delete'
    
    message_success = _('Your comment was deleted successfully.')
    
    def get_context_data(self, **kwargs):
        context = super(CommentDeleteView, self).get_context_data(**kwargs)
        context.update({'note': self.object.note})
        return context
    
    def post(self, request, *args, **kwargs):
        self.comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        self.referer = request.META.get('HTTP_REFERER', self.comment.note.group.get_absolute_url())
        return super(CommentDeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        # self.referer is set in post() method
        messages.success(self.request, self.message_success)
        return self.referer

comment_delete = CommentDeleteView.as_view()


class CommentDetailView(SingleObjectMixin, RedirectView):

    model = Comment

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        return HttpResponseRedirect(obj.get_absolute_url())

comment_detail = CommentDetailView.as_view()


class CommentUpdateView(RequireWriteMixin, FilterGroupMixin, UpdateView):

    form_class = CommentForm
    group_field = 'note__group'
    model = Comment
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super(CommentUpdateView, self).get_context_data(**kwargs)
        context.update({'note': self.object.note})
        return context
    
    def post(self, request, *args, **kwargs):
        self.comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        self.referer = request.META.get('HTTP_REFERER', self.comment.note.group.get_absolute_url())
        return super(CommentUpdateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        # self.referer is set in post() method
        return self.referer

comment_update = CommentUpdateView.as_view()


