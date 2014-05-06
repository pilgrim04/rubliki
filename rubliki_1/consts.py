__author__ = 'pilgrim'
# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

INCOME_TRANSACTION = 1
OUTCOME_TRANSACTION = 2

TRANSACTION_TYPE_CHOICES = (
    (INCOME_TRANSACTION, _('income')),
    (OUTCOME_TRANSACTION, _('outcome')),
)


CASH = 1
CASHLESS = 2

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


DEBIT = 1  # категория, по которой деньги со счета уходят
CREDIT = 2  # категория, по которой деньги на счет поступают
CATEGORY_TYPE_CHOICES = (
    (DEBIT, _('debit')),
    (CREDIT, _('credit')),
)