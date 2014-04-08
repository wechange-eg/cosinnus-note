# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from extra_views import SortableListMixin

from cosinnus.views.attached_object import (CreateViewAttachable,
    UpdateViewAttachable)

from cosinnus.views.mixins.group import (RequireReadMixin, RequireWriteMixin,
    FilterGroupMixin, GroupFormKwargsMixin)
from cosinnus.views.mixins.tagged import TaggedListMixin

from cosinnus_note.forms import CommentForm, NoteForm
from cosinnus_note.models import Note, Comment


class NoteCreateView(RequireWriteMixin, FilterGroupMixin, GroupFormKwargsMixin,
                     CreateViewAttachable):

    form_class = NoteForm
    model = Note
    template_name_suffix = '_create'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        return super(NoteCreateView, self).form_valid(form)

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


class NoteListView(RequireReadMixin, FilterGroupMixin, TaggedListMixin,
                   SortableListMixin, ListView):
    model = Note

    def get(self, request, *args, **kwargs):
        self.sort_fields_aliases = self.model.SORT_FIELDS_ALIASES
        return super(NoteListView, self).get(request, *args, **kwargs)

note_list = NoteListView.as_view()


class NoteUpdateView(RequireWriteMixin, FilterGroupMixin, GroupFormKwargsMixin,
                     UpdateViewAttachable):

    form_class = NoteForm
    model = Note
    template_name_suffix = '_update'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        return super(NoteUpdateView, self).form_valid(form)

note_update = NoteUpdateView.as_view()


class CommentCreateView(RequireWriteMixin, FilterGroupMixin, CreateView):

    form_class = CommentForm
    group_field = 'note__group'
    model = Comment
    template_name_suffix = '_create'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.note = self.note
        return super(CommentCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        context.update({'note': self.note})
        return context

    def get(self, request, *args, **kwargs):
        self.note = get_object_or_404(Note, group=self.group, slug=self.kwargs.get('slug'))
        return super(CommentCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.note = get_object_or_404(Note, group=self.group, slug=self.kwargs.get('slug'))
        return super(CommentCreateView, self).post(request, *args, **kwargs)

comment_create = CommentCreateView.as_view()


class CommentDeleteView(RequireWriteMixin, FilterGroupMixin, DeleteView):

    group_field = 'note__group'
    model = Comment
    template_name_suffix = '_delete'

    def get_context_data(self, **kwargs):
        context = super(CommentDeleteView, self).get_context_data(**kwargs)
        context.update({'note': self.object.note})
        return context

    def get_success_url(self):
        return self.object.note.get_absolute_url()

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

comment_update = CommentUpdateView.as_view()
