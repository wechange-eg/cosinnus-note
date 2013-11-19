# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from cosinnus_note.views import (NoteCreateView, NoteDeleteView,
    NoteDetailView, NoteIndexView, NoteListView, NoteUpdateView,
    CommentCreateView, CommentDeleteView, CommentDetailView,
    CommentUpdateView)
    
    
cosinnus_root_patterns = patterns('', )

cosinnus_group_patterns = patterns('',
    url(r'^list/$',
        NoteListView.as_view(),
        name='note-list'),

    url(r'^list/(?P<tag>[^/]+)/$',
        NoteListView.as_view(),
        name='note-list-filtered'),

    url(r'^create/$',
        NoteCreateView.as_view(),
        name='note-create'),

    url(r'^note/(?P<slug>[^/]+)/$',
        NoteDetailView.as_view(),
        name='note-detail'),

    url(r'^note/(?P<slug>[^/]+)/delete/$',
        NoteDeleteView.as_view(),
        name='note-delete'),

    url(r'^note/(?P<slug>[^/]+)/update/$',
        NoteUpdateView.as_view(),
        name='note-update'),

    url(r'^note/(?P<slug>[^/]+)/comment/$',
        CommentCreateView.as_view(),
        name='note-comment'),

    url(r'^comment/(?P<pk>\d+)/$',
        CommentDetailView.as_view(),
        name='comment-detail'),

    url(r'^comment/(?P<pk>\d+)/delete/$',
        CommentDeleteView.as_view(),
        name='comment-delete'),

    url(r'^comment/(?P<pk>\d+)/update/$',
        CommentUpdateView.as_view(),
        name='comment-update'),

    url(r'^$',
        NoteIndexView.as_view(),
        name='index'),
)


urlpatterns = cosinnus_group_patterns + cosinnus_root_patterns
