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
import datetime


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
        user_categories = Category.objects.filter(user_id=self.request.user.id).order_by('id')
        context['user_categories'] = user_categories
        return context


class AddCategoryView(TemplateView, FormView):
    template_name = 'add-new-category.html'
    form_class = AddCategoryForm

    def get_context_data(self, **kwargs):
        context = super(AddCategoryView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        repeated_names = Category.objects.filter(user=self.request.user,
                                                 category_name=data['category_name'])
        if not repeated_names:
            _ = Category.objects.create(user=self.request.user,
                                        category_name=data['category_name'])
        return HttpResponseRedirect('/my_categories')

    def form_invalid(self, form):
        context = super(AddCategoryView, self).form_invalid(form)
        return context


# class SubcategoryView(TemplateView):
#     template_name = 'subcategories.html'
#
#     def get_context_data(self, category_name,  **kwargs):
#         context = super(SubcategoryView, self).get_context_data(**kwargs)
#         current_category_id = Category.objects.get(user=self.request.user, category_name=category_name).id
#         context['current_subcategories'] = Subcategory.objects.filter(id=current_category_id)
#         context['category_name'] = Category.objects.get(user=self.request.user,
#                                                         category_name=category_name).category_name
#         return context
#
#
# class AddSubcategoryView(TemplateView, FormView):
#     template_name = 'add-new-subcategory.html'
#     form_class = AddSubcategoryForm
#
#     def get_context_data(self, category_name, **kwargs):
#         context = super(AddSubcategoryView, self).get_context_data(**kwargs)
#         current_category_name = Category.objects.get(user=self.request.user, category_name=category_name).category_name
#         context['category_name'] = current_category_name
#         return context
#
#     def form_valid(self, form):
#         data = form.cleaned_data
#         repeated_names = Subcategory.objects.filter(subcategory_name=data['subcategory_name'])
#         if not repeated_names:
#             _ = Subcategory.objects.create(subcategory_name=data['subcategory_name'])
#         return HttpResponseRedirect('/my_categories/')


class TransactionView(TemplateView, FormView):
    template_name = 'transaction.html'
    form_class = TransactionForm

    def get_context_data(self, **kwargs):
        context = super(TransactionView, self).get_context_data(**kwargs)
        context['my_billings'] = Billing.objects.filter(user=self.request.user)
        context['my_categories'] = Category.objects.filter(user=self.request.user).order_by('id')
        context['transaction_types'] = TransactionType.objects.all()
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        _ = Transaction.objects.create(user=self.request.user,
                                       billing=Billing.objects.get(id=data['billing_id']),
                                       transaction_type=TransactionType.objects.get(id=data['transaction_type']),
                                       category=Category.objects.get(id=data['category_id']),
                                       subcategory=Subcategory.objects.get(id=1),
                                       money=data['money'],
                                       datetime=datetime.datetime.now(),
                                       comment=data['comment']
                                       )
        return HttpResponse('/')

    def form_invalid(self, form):
        context = super(TransactionView, self).form_invalid(form)
        return context