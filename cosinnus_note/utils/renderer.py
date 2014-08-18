# -*- coding: utf-8 -*-
"""
Created on 08.07.2014

@author: Sascha Narr
"""
from __future__ import unicode_literals

from cosinnus.utils.renderer import BaseRenderer


class NoteRenderer(BaseRenderer):

    template = 'cosinnus_note/attached_notes.html'
    template_single = 'cosinnus_note/single_note.html'

    @classmethod
    def render(cls, context, myobjs):
        return super(NoteRenderer, cls).render(context, notes=myobjs)
