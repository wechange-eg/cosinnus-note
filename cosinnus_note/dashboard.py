# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from cosinnus.utils.dashboard import DashboardWidget, DashboardWidgetForm

from cosinnus_note.models import Note
from cosinnus_note.views import NoteCreateView
from django.core.exceptions import ImproperlyConfigured
from cosinnus_note.forms import NoteForm


class CompactNotesForm(DashboardWidgetForm):
    amount = forms.IntegerField(label="Amount", initial=5, min_value=0,
        help_text="0 means unlimited", required=False)


class DetailedNotesForm(DashboardWidgetForm):
    amount = forms.IntegerField(label="Amount", initial=3, min_value=0,
        help_text="0 means unlimited", required=False)


class NewNoteForm(forms.ModelForm):

    class Meta:
        fields = ('title', 'text')
        model = Note


class BaseNotesWidget(DashboardWidget):

    app_name = 'note'
    model = Note
    template_name = None
    user_model_attr = None

    def get_data(self):
        count = int(self.config['amount'])
        qs = self.get_queryset().all()

        if count != 0:
            qs = qs[:count]

        data = {
            'notes': qs,
            'group': self.config.group,
            'no_data': _('No news'),
            'widget_id': self.id,
            'widget_title': self.title,
        }

        return render_to_string(self.get_template_name(), data,
                                context_instance=RequestContext(self.request))

    def get_template_name(self):
        if self.template_name is None:
            raise ImproperlyConfigured("No template_name given")
        return self.template_name


class CompactNotes(BaseNotesWidget):
    form_class = CompactNotesForm
    template_name = 'cosinnus_note/widgets/compact_news.html'
    title = _('News')
    widget_name = 'compact news list'


class DetailedNotes(BaseNotesWidget):
    """ This widget acts as a combined group and user widget.
        Group widget: Contains a note-post form and the latest news
        User widget: Contains the latest news posts from all the user's groups.
            Note!: The user note widget need to get the base_widget.html template instead
                    of the fadedown_base_widget.html template as it contains no form!
     """
    
    form_class = DetailedNotesForm
    template_name = 'cosinnus_note/widgets/detailed_news_content.html'
    title = _('Write a news post...')
    widget_name = 'detailed news list'
    
    def __init__(self, request, config_instance):
        super(DetailedNotes, self).__init__(request, config_instance)
        # Adjust title for user widget
        if not self.config.group:
            self.title = _('News stream')
