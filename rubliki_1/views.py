# -*- coding: utf-8 -*-
from django.template.response import TemplateResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.generic import FormView
from django.http import HttpResponseRedirect, HttpResponse
from .forms import *


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            raise Exception('Already login')
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect('/')
