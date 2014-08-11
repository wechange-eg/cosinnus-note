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

from extra_views import SortableListMixin

from cosinnus.views.attached_object import (CreateViewAttachable,
    UpdateViewAttachable)

from cosinnus.views.mixins.group import (RequireReadMixin, RequireWriteMixin,
    FilterGroupMixin, GroupFormKwargsMixin)
from cosinnus.views.mixins.user import UserFormKwargsMixin

from cosinnus_note.forms import CommentForm, NoteForm
from cosinnus_note.models import Note, Comment
from django.contrib import messages


class NoteCreateView(RequireWriteMixin, FilterGroupMixin, GroupFormKwargsMixin,
                     UserFormKwargsMixin, CreateViewAttachable):

    form_class = NoteForm
    model = Note
    template_name_suffix = '_create'
    
    message_success = _('Your news post was added successfully.')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, self.message_success)
        return super(NoteCreateView, self).form_valid(form)
    
    def form_invalid(self, form):
        """
        If the form is invalid, we simply redirect to the success url anyway.
        """
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.referer = request.META.get('HTTP_REFERER', reverse('cosinnus:note:list', kwargs={'group':self.group}))
        return super(NoteCreateView, self).post(request, *args, **kwargs)
    
    def get_success_url(self):
        # self.referer is set in post() method
        return self.referer

note_create = NoteCreateView.as_view()


class NoteDeleteView(RequireWriteMixin, FilterGroupMixin, DeleteView):

    model = Note
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse('cosinnus:note:list', kwargs={'group': self.group.slug})

note_delete = NoteDeleteView.as_view()


class NoteDetailView(RequireReadMixin, FilterGroupMixin, DetailView):

    model = Note

note_detail = NoteDetailView.as_view()


class NoteIndexView(RequireReadMixin, RedirectView):

    def get_redirect_url(self, **kwargs):
        return reverse('cosinnus:note:list', kwargs={'group': self.group.slug})

note_index = NoteIndexView.as_view()


class NoteListView(RequireReadMixin, FilterGroupMixin, ListView):
    model = Note
    
    def get_context_data(self, **kwargs):
        kwargs.update({
            'form':  NoteForm(group=self.group)
        })
        return super(NoteListView, self).get_context_data(**kwargs)

note_list = NoteListView.as_view()


class NoteUpdateView(RequireWriteMixin, FilterGroupMixin, GroupFormKwargsMixin,
                     UserFormKwargsMixin, UpdateViewAttachable):

    form_class = NoteForm
    model = Note
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse('cosinnus:note:list', kwargs={'group': self.group.slug})

note_update = NoteUpdateView.as_view()


class CommentCreateView(RequireWriteMixin, FilterGroupMixin, CreateView):

    form_class = CommentForm
    group_field = 'note__group'
    model = Comment
    template_name_suffix = '_create'
    
    message_success = _('Your comment was added successfully.')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.note = self.note
        messages.success(self.request, self.message_success)
        return super(CommentCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        context.update({'note': self.note})
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
