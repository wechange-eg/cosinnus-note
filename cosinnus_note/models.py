# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from embed_video.fields import EmbedVideoField

from cosinnus.utils.functions import unique_aware_slugify
from cosinnus.models.tagged import BaseTaggableObjectModel



class Note(BaseTaggableObjectModel):
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
        super(Note, self).save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {'group': self.group.slug, 'slug': self.slug}
        return reverse('cosinnus:note:note', kwargs=kwargs)


@python_2_unicode_compatible
class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), on_delete=models.PROTECT)
    created_on = models.DateTimeField(_('Created'), auto_now_add=True, editable=False)
    note = models.ForeignKey(Note, related_name='comments')
    text = models.TextField(_('Text'))

    class Meta:
        ordering = ['created_on']
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        return 'Comment on “%(note)s” by %(author)s' % {
            'note': self.note.title,
            'author': self.author.get_full_name(),
        }

    def get_absolute_url(self):
        return '%s#comment-%d' % (self.note.get_absolute_url(), self.pk)


import django
if django.VERSION[:2] < (1, 7):
    from cosinnus_note import cosinnus_app
    cosinnus_app.register()
