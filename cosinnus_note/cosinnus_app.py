# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def register():
    # Import here to prevent import side effects
    from django.utils.translation import ugettext_lazy as _

    from cosinnus.core.registries import (app_registry, url_registry,
        widget_registry)

    from cosinnus_note.urls import (cosinnus_group_patterns,
        cosinnus_root_patterns)

    app_registry.register('cosinnus_note', 'note', _('Notes'))
    url_registry.register('cosinnus_note', cosinnus_root_patterns,
        cosinnus_group_patterns)
    for w in ('CompactNotes', 'DetailedNotes',):
        widget_registry.register('note', 'cosinnus_note.dashboard.%s' % w)
