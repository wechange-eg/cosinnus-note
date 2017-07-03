# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.dispatch as dispatch
from django.utils.translation import ugettext_lazy as _

""" Cosinnus:Notifications configuration file. 
    See http://git.sinnwerkstatt.com/cosinnus/cosinnus-core/wikis/cosinnus-notifications-guidelines.
"""

""" Signal definitions """
note_comment_posted_on_any = dispatch.Signal(providing_args=["user", "obj", "audience"])
note_comment_posted = dispatch.Signal(providing_args=["user", "obj", "audience"])
note_comment_posted_on_commented_post = dispatch.Signal(providing_args=["user", "obj", "audience"])
note_created = dispatch.Signal(providing_args=["user", "obj", "audience"])


""" Notification definitions.
    These will be picked up by cosinnus_notfications automatically, as long as the 
    variable 'notifications' is present in the module '<app_name>/cosinnus_notifications.py'.
    
    Both the mail and subject template will be provided with the following context items:
        :receiver django.auth.User who receives the notification mail
        :sender django.auth.User whose action caused the notification to trigger
        :receiver_name Convenience, full name of the receiver
        :sender_name Convenience, full name of the sender
        :object The object that was created/changed/modified and which the notification is about.
        :object_url The url of the object, if defined by get_absolute_url()
        :object_name The title of the object (only available if it is a BaseTaggableObject)
        :group_name The name of the group the object is housed in (only available if it is a BaseTaggableObject)
        :site_name Current django site's name
        :domain_url The complete base domain needed to prefix URLs. (eg: 'http://sinnwerkstatt.com')
        :notification_settings_url The URL to the cosinnus notification settings page.
        :site Current django site
        :protocol Current portocol, 'http' or 'https'
        
    
""" 
notifications = {
    'note_comment_posted_on_any': {
        'label': _('A user commented on a news post'), 
        'mail_template': 'cosinnus_note/notifications/note_comment_posted.html',
        'subject_template': 'cosinnus_note/notifications/note_comment_posted_subject.txt',
        'signals': [note_comment_posted_on_any],
        'default': False,
        
        'is_html': True,
        'snippet_type': 'news',
        'event_text': _('%(sender_name)s commented on a news post'),
        'notification_text': _('%(sender_name)s commented on a news post'),
        'subject_text': _('%(sender_name)s commented on a news post'),
        'sub_event_text': _('%(sender_name)s'),
        'data_attributes': {
            'object_name': 'note.get_readable_title', 
            'object_url': 'get_absolute_url', 
            'image_url': 'note.creator.cosinnus_profile.get_avatar_thumbnail_url', # note: receiver avatar, not creator's!
            # no event in comment meta for now. looks ugly
            #'sub_event_meta': 'created_on', # created date
            'sub_image_url': 'creator.cosinnus_profile.get_avatar_thumbnail_url', # the comment creators
            'sub_object_text': 'text',
        },
    },  
    'note_comment_posted': {
        'label': _('A user commented on one of your news posts'), 
        'mail_template': 'cosinnus_note/notifications/note_comment_posted.html',
        'subject_template': 'cosinnus_note/notifications/note_comment_posted_subject.txt',
        'signals': [note_comment_posted],
        'default': True,
        
        'is_html': True,
        'snippet_type': 'news',
        'event_text': _('%(sender_name)s commented on your news post'),
        'notification_text': _('%(sender_name)s commented on one of your news posts'),
        'subject_text': _('%(sender_name)s commented on one of your news posts'),
        'sub_event_text': _('%(sender_name)s'),
        'data_attributes': {
            'object_name': 'note.get_readable_title', 
            'object_url': 'get_absolute_url', 
            'image_url': 'note.creator.cosinnus_profile.get_avatar_thumbnail_url', # note: receiver avatar, not creator's!
            # no event in comment meta for now. looks ugly
            #'sub_event_meta': 'created_on', # created date
            'sub_image_url': 'creator.cosinnus_profile.get_avatar_thumbnail_url', # the comment creators
            'sub_object_text': 'text',
        },
    },  
    'note_comment_posted_in_commented_post': {
        'label': _('A user commented on a news posts you commented in'), 
        'mail_template': 'cosinnus_note/notifications/note_comment_posted_on_commented_post.html',
        'subject_template': 'cosinnus_note/notifications/note_comment_posted_on_commented_post_subject.txt',
        'signals': [note_comment_posted_on_commented_post],
        'default': True,
        
        'is_html': True,
        'snippet_type': 'news',
        'event_text': _('%(sender_name)s commented on a news post you commented in'),
        'subject_text': _('%(sender_name)s commented on a news post you commented in'),
        'sub_event_text': _('%(sender_name)s'),
        'data_attributes': {
            'object_name': 'note.get_readable_title', 
            'object_url': 'get_absolute_url', 
            'image_url': 'note.creator.cosinnus_profile.get_avatar_thumbnail_url', # note: receiver avatar, not creator's!
            # no event in comment meta for now. looks ugly
            #'sub_event_meta': 'created_on', # created date
            'sub_image_url': 'creator.cosinnus_profile.get_avatar_thumbnail_url', # the comment creators
            'sub_object_text': 'text',
        },
    },  
    'note_created': {
        'label': _('A user created a news post'), 
        'mail_template': 'cosinnus_note/notifications/note_created.txt',
        'subject_template': 'cosinnus_note/notifications/note_created_subject.txt',
        'signals': [note_created],
        'default': True,
        
        'is_html': True,
        'snippet_type': 'news',
        'event_text': _('New news post by %(sender_name)s'),
        'notification_text': _('%(sender_name)s created a new news post'),
        'subject_text': _('%(sender_name)s posted in %(team_name)s:'),
        'data_attributes': {
            'object_name': 'get_readable_title', 
            'object_url': 'get_absolute_url', 
            'object_text': 'text',
        },
    },  
}
