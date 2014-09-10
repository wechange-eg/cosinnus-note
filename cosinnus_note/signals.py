# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import get_connection, EmailMessage
from django.template.loader import render_to_string

from cosinnus.conf import settings


import django.dispatch as dispatch

""" Called when a user posts a comment on a news post """
note_comment_posted = dispatch.Signal(providing_args=["group", "user", "note", "comment"])


# we need to load the receivers for them to be active
import receivers
