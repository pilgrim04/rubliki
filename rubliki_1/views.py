# -*- coding: utf-8 -*-
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.generic import FormView, RedirectView
from coffin.views.generic.base import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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
        auth_logout(self.request)
        return super(LogoutView, self).get(*args, **kwargs)


class EditProfileView(TemplateView):
    template_name = 'edit.html'

    def get_context_data(self, **kwargs):
        context = super(EditProfileView, self).get_context_data(**kwargs)
        return context


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration.html'

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.create_user(data['login'],
                                        data['email'],
                                        data['password'],
                                        first_name=data['first_name'],
                                        last_name=data['last_name'])
        user.save()
        #TODO: настроить автоматическое попадание в личный кабинет после регистрации
        return HttpResponseRedirect('/login')


class CabinetView(TemplateView):
    template_name = 'cabinet.html'
    #TODO: настроить декоратор

    def get_context_data(self, **kwargs):
        context = super(CabinetView, self).get_context_data(**kwargs)
        if self.request.user.first_name:
            context['current_user'] = self.request.user.first_name
        else:
            context['current_user'] = self.request.user
        return context


class BillingView(TemplateView):
    template_name = 'billings.html'

    def get_context_data(self, **kwargs):
        context = super(BillingView, self).get_context_data(**kwargs)
        user_billings = Billing.objects.filter(user_id=self.request.user.id)
        context['user_billings'] = user_billings
        return context


class AddBillingView(TemplateView, FormView):
    template_name = 'add-new-billing.html'
    form_class = AddBillingForm

    def get_context_data(self, **kwargs):
        context = super(AddBillingView, self).get_context_data(**kwargs)
        context['billing_type'] = BillingTypes.objects.all()
        context['currency'] = Currency.objects.all()
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        repeated_names = Billing.objects.filter(user=self.request.user,
                                                billing_name=data['billing_name'])
        if not repeated_names:
            _ = Billing.objects.create(user=self.request.user,
                                       billing_name=data['billing_name'],
                                       billing_type=BillingTypes.objects.get(billing_type=data['billing_type']),
                                       currency=Currency.objects.get(currency=data['currency']),
                                       money=data['money'])
        return HttpResponseRedirect('/my_billings')

    def form_invalid(self, form):
        context = super(AddBillingView, self).form_invalid(form)
        return context


class CategoryView(TemplateView):
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        return context

