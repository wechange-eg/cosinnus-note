# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from markupfield.fields import MarkupField

from cosinnus.authentication.models import Group, User
from cosinnus.utils.functions import unique_aware_slugify
from cosinnus.utils.models import TaggableModel


class Note(TaggableModel):

    SORT_FIELDS_ALIASES = [
        ('title', 'title'), ('author', 'author'), ('created_on', 'created_on'),
    ]

    created_on = models.DateTimeField(_(u'Created'), auto_now_add=True, editable=False)
    author = models.ForeignKey(User, verbose_name=_(u'Author'),
                               on_delete=models.PROTECT, related_name='notes')
    group = models.ForeignKey(Group, verbose_name=_(u'Group'))
    slug = models.SlugField(max_length=145)  # 4 numbers for the slug number should be fine
    text = MarkupField(_(u'Text'), default_markup_type='plain')
    title = models.CharField(_(u'Title'), max_length=140)

    class Meta:
        ordering = ['-created_on', 'title']
        unique_together = ('group', 'slug')
        verbose_name = _('Note')
        verbose_name_plural = _('Notes')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_aware_slugify(self, slug_source='title', slug_field='slug', group=self.group)
        super(Note, self).save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {'group': self.group.pk, 'slug': self.slug}
        return reverse('note-detail', kwargs=kwargs)


class Comment(models.Model):

    author = models.ForeignKey(User, verbose_name=_(u'Author'), on_delete=models.PROTECT)
    created_on = models.DateTimeField(_(u'Created'), auto_now_add=True, editable=False)
    note = models.ForeignKey(Note, related_name='comments')
    text = MarkupField(_(u'Text'), default_markup_type='plain')

    class Meta:
        ordering = ['created_on']
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __unicode__(self):
        return u'Comment on “%(note)s” by %(author)s' % {
            'note': self.note.title,
            'author': self.author.get_full_name(),
        }

    def get_absolute_url(self):
        return '%s#comment-%d' % (self.note.get_absolute_url(), self.pk)
