'''
Created on 05.08.2014

@author: Sascha
'''
from django.utils.translation import ugettext_lazy as _

from cosinnus.views.mixins.filters import CosinnusFilterSet
from cosinnus.forms.filters import AllObjectsFilter, SelectCreatorWidget,\
    DropdownChoiceWidget
from django_filters.filters import ChoiceFilter
from django.core.exceptions import ImproperlyConfigured
from cosinnus_note.models import Note
from django.db.models.aggregates import Count


class NoteFilter(CosinnusFilterSet):
    creator = AllObjectsFilter(label=_('Created By'), widget=SelectCreatorWidget)
    
    class Meta:
        model = Note
        fields = ['creator']
        order_by = (
            ('-created', _('Newest Created')),
            ('-num_comments', _('Popularity')),
        )
        
    @property
    def qs(self):
        if not hasattr(self, '_qs') and hasattr(self, 'queryset'):
            self.queryset = self.queryset.annotate(num_comments=Count('comments'))
        return super(NoteFilter, self).qs
    
    def get_order_by(self, order_value):
        return super(NoteFilter, self).get_order_by(order_value)
    