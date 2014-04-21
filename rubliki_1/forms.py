__author__ = 'pilgrim'
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _


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
