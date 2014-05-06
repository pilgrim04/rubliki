__author__ = 'pilgrim'
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from .models import User, Billing
from .consts import *


class LoginForm(forms.Form):
    login = forms.CharField(label=_("Login"), )
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    user_cache = None

    def clean(self):
        login = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')

        if login and password:
            self.user_cache = authenticate(username=login, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    _("Please enter a correct username and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class RegistrationForm(forms.Form):
    login = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    password_confirm = forms.CharField(max_length=30, widget=forms.PasswordInput())

    first_name = forms.CharField()
    last_name = forms.CharField()

    def clean_password_confirm(self):
        password_confirm = self.cleaned_data['password_confirm']
        if password_confirm != self.cleaned_data.get('password'):
            raise forms.ValidationError(_('Passwords must be equal'))
        return password_confirm

    def clean(self):
        data = self.cleaned_data
        existing = User.objects.filter(username__iexact=data['login'])
        if existing.exists():
            self.errors['login'] = [_('This login is already registered')]
            del data['login']

        existing = User.objects.filter(email__iexact=data['email'])
        if existing.exists():
            self.errors['email'] = [_('This email is already registered')]
            del data['email']
        return data


class AddBillingForm(forms.Form):
    billing_name = forms.CharField(label=(_("billing_name")))
    billing_type = forms.IntegerField(label=(_("billing_type")))
    currency = forms.IntegerField(label=(_("currency")))
    money = forms.FloatField(label=(_("money")))


class AddCategoryForm(forms.Form):
    category_name = forms.CharField(label=(_("category_name")))
    category_type = forms.IntegerField(label=(_("category_type")))


# class AddSubcategoryForm(forms.Form):
#     subcategory_name = forms.CharField(label=(_("subcategory_name")))
#
#     # def __init__(self, current_category_id, *args, **kwargs):
#     #     return super(AddSubcategoryForm, self).__init__(current_category_id, *args, **kwargs)


class TransactionForm(forms.Form):
    billing_id = forms.IntegerField(label=(_("billing_id")))
    category_id = forms.IntegerField(label=(_("category_id")))
    transaction_type = forms.IntegerField(label=(_("transaction_type")))
    money = forms.FloatField(label=(_("money")))
    comment = forms.CharField(label=(_("comment")))


class TransferForm(forms.Form):
    billing_id_from = forms.IntegerField(label=(_("billing_id_from")))
    billing_id_to = forms.IntegerField(label=(_("billing_id_to")))
    money = forms.FloatField(label=(_("money")))
    comment = forms.CharField(label=(_("comment")))