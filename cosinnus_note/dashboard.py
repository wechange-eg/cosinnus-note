# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from cosinnus.utils.dashboard import DashboardWidget, DashboardWidgetForm

from cosinnus_note.models import Note

class CompactNotesForm(DashboardWidgetForm):
    amount = forms.IntegerField(label="Amount", initial=5, min_value=0,
        help_text="0 means unlimited", required=False)


class CompactNotes(DashboardWidget):

    app_name = 'note'
    form_class = CompactNotesForm
    model = Note
    title = _('News')
    user_model_attr = None
    widget_name = 'compact news list'

    def get_data(self):
        count = int(self.config['amount'])
        qs = self.get_queryset().values_list('title', 'created', 'slug', 'group').all()
        if count != 0:
            qs = qs[:count]
        data = {
            'notes': [dict(zip(['title', 'date', 'slug', 'group'], note)) for note in qs],
            'no_data': _('No news'),
        }
        return render_to_string('cosinnus_note/widgets/compact_news.html', data)

class DetailedNotesForm(DashboardWidgetForm):
    amount = forms.IntegerField(label="Amount", initial=3, min_value=0,
        help_text="0 means unlimited", required=False)


class DetailedNotes(DashboardWidget):

    app_name = 'note'
    form_class = DetailedNotesForm
    model = Note
    title = _('Detailed News')
    user_model_attr = None
    widget_name = 'detailed news list'

    def get_data(self):
        count = int(self.config['amount'])
        qs = self.get_queryset().all()

        if count != 0:
            qs = qs[:count]
        data = {
            'notes': qs,
            'no_data': _('No news'),
        }
        return render_to_string('cosinnus_note/widgets/detailed_news.html', data)

