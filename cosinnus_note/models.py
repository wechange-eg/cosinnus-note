# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

import logging
logger = logging.getLogger('cosinnus')

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from embed_video.fields import EmbedVideoField

from cosinnus.utils.functions import unique_aware_slugify
from cosinnus.models.tagged import BaseTaggableObjectModel
from django.utils.functional import cached_property
from cosinnus.utils.permissions import filter_tagged_object_queryset_for_user
from cosinnus.utils.urls import group_aware_reverse
from cosinnus_note import cosinnus_notifications
from django.contrib.auth import get_user_model


class Note(BaseTaggableObjectModel):
    
    EMPTY_TITLE_PLACEHOLDER = '---'
    
    SORT_FIELDS_ALIASES = [
        ('title', 'title'), ('creator', 'creator'), ('created', 'created'),
    ]

    text = models.TextField(_('Text'))
    video = EmbedVideoField(blank=True, null=True)

    class Meta(BaseTaggableObjectModel.Meta):
        ordering = ['-created', 'title']
        verbose_name = _('Note')
        verbose_name_plural = _('Notes')

    def __init__(self, *args, **kwargs):
        super(Note, self).__init__(*args, **kwargs)
        self._meta.get_field('creator').verbose_name = _('Author')

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_aware_slugify(self, slug_source='title', slug_field='slug', group=self.group)
        created = bool(self.pk) == False
        
        # take the first youtube url from the textand save it as a video link
        self.video = None
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.text)
        for url in urls:
            if 'youtube.com' in url:
                self.video = url
                break
            
        super(Note, self).save(*args, **kwargs)
        if created:
            # todo was created
            audience = get_user_model().objects.filter(id__in=self.group.members).exclude(id=self.creator.pk)
            log_msg = "A note with id", self.pk, "was created. Triggering a notification for possible members \
                    (depending on their preferences): ", ",".join([aud.email for aud in audience])
            logger.info(log_msg)
            cosinnus_notifications.note_created.send(sender=self, user=self.creator, obj=self, audience=audience)
        

    def get_absolute_url(self):
        kwargs = {'group': self.group.slug, 'slug': self.slug}
        return group_aware_reverse('cosinnus:note:note', kwargs=kwargs)
    
    @classmethod
    def get_current(self, group, user):
        """ Returns a queryset of the current upcoming events """
        qs = Note.objects.filter(group=group)
        if user:
            qs = filter_tagged_object_queryset_for_user(qs, user)
        return qs
    
    @cached_property
    def video_id(self):
        """ Returns the video id from a URL as such:
        http://www.youtube.com/watch?v=CENF14Iloxw&hq=1
        """
        if self.video:
            match = re.search(r'[?&]v=([a-zA-Z0-9-_]+)(&|$)', self.video)
            if match:
                vid = match.groups()[0]
                return vid
        return None

    @property
    def video_thumbnail(self):
        vid = self.video_id
        ret = None
        if vid:
            ret = 'http://img.youtube.com/vi/%s/hqdefault.jpg' % vid
        return ret


@python_2_unicode_compatible
class Comment(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Creator'), on_delete=models.PROTECT)
    created_on = models.DateTimeField(_('Created'), auto_now_add=True, editable=False)
    note = models.ForeignKey(Note, related_name='comments')
    text = models.TextField(_('Text'))

    class Meta:
        ordering = ['created_on']
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return 'Comment on “%(note)s” by %(creator)s' % {
            'note': self.note.title,
            'creator': self.creator.get_full_name(),
        }

    def get_absolute_url(self):
        if self.pk:
            return '%s#comment-%d' % (self.note.get_absolute_url(), self.pk)
        return self.note.get_absolute_url()
    
    def save(self, *args, **kwargs):
        created = bool(self.pk) == False
        super(Comment, self).save(*args, **kwargs)
        if created:
            # comment was created
            if not self.note.creator == self.creator:
                cosinnus_notifications.note_comment_posted.send(sender=self, user=self.creator, obj=self, audience=[self.note.creator])
    
    @property
    def group(self):
        """ Needed by the notifications system """
        return self.note.group

import django
if django.VERSION[:2] < (1, 7):
    from cosinnus_note import cosinnus_app
    cosinnus_app.register()
