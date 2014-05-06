# -*- coding: utf-8 -*-
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.generic import FormView, RedirectView
from coffin.views.generic.base import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
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
        return HttpResponseRedirect('/my_billings')

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
        return HttpResponseRedirect('/cabinet')


class CabinetView(TemplateView):
    template_name = 'cabinet.html'
    #TODO: настроить декоратор

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated() or self.request.user.is_anonymous():
            # return HttpResponseRedirect(reverse('login'))
            raise ValueError('You are not log in. Please do it.')
        context = super(CabinetView, self).get_context_data(**kwargs)
        if self.request.user.first_name:
            context['current_user'] = self.request.user.first_name
        else:
            context['current_user'] = self.request.user

        context['balances'] = Billing.objects.filter(user=self.request.user)
        common_balance = 0
        for i in Billing.objects.filter(user=self.request.user):
            common_balance += i.money
        context['common_balance'] = common_balance
        #TODO: складываю абсолютные значения, не учитывая валюту
        context['qty_of_balances'] = Billing.objects.filter(user=self.request.user).count()
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
        user_categories = Category.objects.filter(user_id__in=(self.request.user.id, 1)).order_by('id')
        context['user_categories'] = user_categories

        return context


class AddCategoryView(TemplateView, FormView):
    template_name = 'add-new-category.html'
    form_class = AddCategoryForm

    def get_context_data(self, **kwargs):
        context = super(AddCategoryView, self).get_context_data(**kwargs)
        context['category_type'] = CategoryTypes.objects.all()
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        repeated_names = Category.objects.filter(user=self.request.user,
                                                 category_name=data['category_name'])
        if not repeated_names:
            _ = Category.objects.create(user=self.request.user,
                                        category_name=data['category_name'],
                                        category_type=CategoryTypes.objects.get(category_type=data['category_type']))
        return HttpResponseRedirect('/my_categories')

    def form_invalid(self, form):
        context = super(AddCategoryView, self).form_invalid(form)
        return context

# # ------------SUB------------------------
#
#
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
# # ------------SUB------------------------

class TransactionView(TemplateView, FormView):
    template_name = 'transaction.html'
    form_class = TransactionForm

    def get_context_data(self, **kwargs):
        context = super(TransactionView, self).get_context_data(**kwargs)
        context['my_billings'] = Billing.objects.filter(user=self.request.user)
        context['my_categories'] = Category.objects.filter(user__in=(self.request.user, 1)).order_by('id')
        context['transaction_types'] = TransactionType.objects.all()
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        # записать факт транзакции
        _ = Transaction.objects.create(user=self.request.user,
                                       billing=Billing.objects.get(id=data['billing_id']),
                                       transaction_type=TransactionType.objects.get(id=data['transaction_type']),
                                       category=Category.objects.get(id=data['category_id']),
                                       # subcategory=Subcategory.objects.get(id=1),
                                       money=data['money'],
                                       datetime=datetime.datetime.now(),
                                       comment=data['comment']
                                       )

        # изменить количество денег на счету
        balance = Billing.objects.get(id=data['billing_id']).money
        if data['transaction_type'] == 1:
            balance += data['money']
        if data['transaction_type'] == 2:
            balance -= data['money']
        Billing.objects.filter(id=data['billing_id']).update(money=balance)

        return HttpResponseRedirect('/statement')

    def form_invalid(self, form):
        context = super(TransactionView, self).form_invalid(form)
        return context


class TransferView(TemplateView, FormView):
    template_name = 'transfer.html'
    form_class = TransferForm

    def get_context_data(self, **kwargs):
        context = super(TransferView, self).get_context_data(**kwargs)
        context['my_billings'] = Billing.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        Transaction.objects.create(user=self.request.user,
                                   billing=Billing.objects.get(id=data['billing_id_from']),
                                   transaction_type=TransactionType.objects.get(id=2),
                                   category=Category.objects.get(id=2),
                                   money=data['money'],
                                   datetime=datetime.datetime.now(),
                                   comment=data['comment'])
        balance = Billing.objects.get(id=data['billing_id_from']).money
        balance -= data['money']
        Billing.objects.filter(id=data['billing_id_from']).update(money=balance)

        Transaction.objects.create(user=self.request.user,
                                   billing=Billing.objects.get(id=data['billing_id_to']),
                                   transaction_type=TransactionType.objects.get(id=1),
                                   category=Category.objects.get(id=1),
                                   money=data['money'],
                                   datetime=datetime.datetime.now(),
                                   comment=data['comment'])
        balance = Billing.objects.get(id=data['billing_id_to']).money
        balance += data['money']
        Billing.objects.filter(id=data['billing_id_to']).update(money=balance)

        return HttpResponseRedirect('/statement')

    def form_invalid(self, form):
        context = super(TransferView, self).form_invalid(form)
        return context


class StatementView(TemplateView):
    template_name = 'statement.html'

    def get_context_data(self, **kwargs):
        context = super(StatementView, self).get_context_data(**kwargs)
        context['transactions'] = Transaction.objects.filter(user=self.request.user)
        context['total_income'] = 0
        context['total_spent'] = 0
        for i in Transaction.objects.filter(user=self.request.user):
            if i.transaction_type_id == 1:
                context['total_income'] += i.money
            if i.transaction_type_id == 2:
                context['total_spent'] -= i.money
        return context