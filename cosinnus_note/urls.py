# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

cosinnus_root_patterns = patterns('cosinnus_note.views', 
    url(r'^notes/embed/all/$',
        'note_embed_global',
        name='embed-global'),
                                  
    url(r'^notes/embed/$',
        'note_embed_current_portal',
        name='embed-current-portal'),
)
    
cosinnus_group_patterns = patterns('cosinnus_note.views',
    url(r'^$',
        'note_index',
        name='index'),

    url(r'^list/$',
        'note_list',
        name='list'),
                                   
    url(r'^embed/$',
        'note_embed',
        name='embed'),

    #url(r'^list/(?P<tag>[^/]+)/$',
    #    'note_list',
    #    name='list-filtered'),

    url(r'^add/$',
        'note_create',
        name='add'),

    url(r'^(?P<slug>[^/]+)/$',
        'note_detail',
        name='note'),

    url(r'^(?P<slug>[^/]+)/delete/$',
        'note_delete',
        name='delete'),

    url(r'^(?P<slug>[^/]+)/update/$',
        'note_update',
        name='update'),

    url(r'^(?P<note_slug>[^/]+)/comment/$',
        'comment_create',
        name='comment'),

    url(r'^comment/(?P<pk>\d+)/$',
        'comment_detail',
        name='comment-detail'),

    url(r'^comment/(?P<pk>\d+)/delete/$',
        'comment_delete',
        name='comment-delete'),

    url(r'^comment/(?P<pk>\d+)/update/$',
        'comment_update',
        name='comment-update'),
                                   
)


urlpatterns = cosinnus_group_patterns + cosinnus_root_patterns
