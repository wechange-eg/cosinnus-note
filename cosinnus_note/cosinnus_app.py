# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

IS_COSINNUS_APP = True
COSINNUS_APP_NAME = 'note'
COSINNUS_APP_LABEL = _('Notes')

DASHBOARD_WIDGETS = ['cosinnus_note.dashboard.CompactNotes', 'cosinnus_note.dashboard.DetailedNotes']
