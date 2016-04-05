# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.http.response import HttpResponseNotAllowed, HttpResponse,\
    HttpResponseForbidden


def save_auth_tokens(request):
    """ Saves the given facebook auth tokens for the current user """
    
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_authenticated():
        return HttpResponseForbidden('Must be logged in!')
    
    
    