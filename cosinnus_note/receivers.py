# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cosinnus.conf import settings
from django.dispatch.dispatcher import receiver

from cosinnus_note.signals import note_comment_posted
from cosinnus.core.mail import get_common_mail_context, send_mail_or_fail


@receiver(note_comment_posted)
def send_note_comment_mail(sender, group, user, note, comment, **kwargs):
    context = get_common_mail_context(sender.request, group=group, user=user)
    creator = note.creator
    context.update({
        'note': note,
        'note_text': note.text,
        'comment_text': comment.text,
        'creator_name': creator.get_full_name() or creator.get_username(),
    })
    subject = _('%(group_name)s: %(user_name)s has commented on one of your news posts on %(site_name)s!')
    send_mail_or_fail(creator.email, subject % context, 'cosinnus_note/mail/note_comment_posted.html', context)
                
                

