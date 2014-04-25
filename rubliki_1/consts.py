__author__ = 'pilgrim'
# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

INCOME_TRANSACTION = True
OUTCOME_TRANSACTION = False

TRANSACTION_TYPE_CHOICES = (
    (INCOME_TRANSACTION, _('income')),
    (OUTCOME_TRANSACTION, _('outcome')),
)


CASH = True
CASHLESS = False

BILLING_TYPE_CHOICES = (
    (CASH, _('cash')),
    (CASHLESS, _('cashless'))
)



RUR = 1
USD = 2
EUR = 3
CURRENCY_CHOICES = (
    (RUR, _('rur')),
    (USD, _('usd')),
    (EUR, _('eur'))
)