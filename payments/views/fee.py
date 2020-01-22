# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from payments.forms.FeeComment import FeeCommentForm


def add_fee_comment(request):

    if request.method == "POST":
        form = FeeCommentForm(request.POST,)
        if form.is_valid():
            redirect_url = form.cleaned_data['redirect_to']
            comment = form.save(commit=False)
            comment.completed_by = request.user
            comment.save()
            messages.success(request, _('Comentario añadido correctamente.'))
            return redirect(redirect_url)