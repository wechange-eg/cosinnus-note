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

from cosinnus.authentication.views import FilterGroupMixin, RequireGroupMixin
from cosinnus.utils.views import TaggedListMixin

from cosinnus_note.forms import CommentForm, NoteForm
from cosinnus_note.models import Note, Comment


class NoteCreateView(RequireGroupMixin, FilterGroupMixin, CreateView):

    form_class = NoteForm
    model = Note
    template_name_suffix = '_create'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.group = self.group
        return super(NoteCreateView, self).form_valid(form)


class NoteDeleteView(RequireGroupMixin, FilterGroupMixin, DeleteView):

    model = Note
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse('note-list', kwargs={'group': self.group.pk})


class NoteDetailView(RequireGroupMixin, FilterGroupMixin, DetailView):

    model = Note


class NoteIndexView(RequireGroupMixin, RedirectView):
    def get_redirect_url(self, **kwargs):
        return reverse('note-list', kwargs={'group': self.group.pk})


class NoteListView(RequireGroupMixin, FilterGroupMixin, TaggedListMixin,
                   SortableListMixin, ListView):
    model = Note


class NoteUpdateView(RequireGroupMixin, FilterGroupMixin, UpdateView):

    form_class = NoteForm
    model = Note
    template_name_suffix = '_update'


class CommentCreateView(RequireGroupMixin, FilterGroupMixin, CreateView):

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


class CommentDeleteView(RequireGroupMixin, FilterGroupMixin, DeleteView):

    group_field = 'note__group'
    model = Comment
    template_name_suffix = '_delete'

    def get_context_data(self, **kwargs):
        context = super(CommentDeleteView, self).get_context_data(**kwargs)
        context.update({'note': self.object.note})
        return context

    def get_success_url(self):
        return self.object.note.get_absolute_url()


class CommentDetailView(SingleObjectMixin, RedirectView):

    model = Comment

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        return HttpResponseRedirect(obj.get_absolute_url())


class CommentUpdateView(RequireGroupMixin, FilterGroupMixin, UpdateView):

    form_class = CommentForm
    group_field = 'note__group'
    model = Comment
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super(CommentUpdateView, self).get_context_data(**kwargs)
        context.update({'note': self.object.note})
        return context
