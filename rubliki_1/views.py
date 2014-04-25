# -*- coding: utf-8 -*-
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.generic import FormView, RedirectView
from coffin.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from .forms import *


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            raise Exception('Already login')
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect('/cabinet')

    def form_invalid(self, form):
        context = super(LoginView, self).form_invalid(form)
        return context


class LogoutView(TemplateView):
    template_name = 'logout.html'

    def get(self, *args, **kwargs):
        print 'def logout'
        auth_logout(self.request)
        return super(LogoutView, self).get(*args, **kwargs)


class CabinetView(TemplateView):
    template_name = 'cabinet.html'

    def get_context_data(self, **kwargs):
        context = super(CabinetView, self).get_context_data(**kwargs)
        if self.request.user.first_name:
            context['user'] = self.request.user.first_name
        else:
            context['user'] = self.request.user
        return context