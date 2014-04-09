# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    username = models.CharField(max_length=256, unique=True)
    email = models.CharField(max_length=256)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    birth_date = models.DateField()


class Currency(models.Model):  # валюта. 1 - rur, 2 - usd, 3 - eur
    currency = models.CharField(max_length=3)


class BillingTypes(models.Model):  # типы счетов. 1 - cash, 2 - cashless
    billing_type = models.CharField(max_length=20)


class Billing(models.Model):
    user = models.ForeignKey(User)
    billing_name = models.CharField(max_length=256)
    billing_type = models.ForeignKey(BillingTypes)
    currency = models.ForeignKey(Currency)


class Category(models.Model):  # категории приходов-расходов
    category_name = models.CharField(max_length=256)
    user = models.ForeignKey(User)  # привязка к юзеру, который создал категорию


class Subcategory(models.Model):
    category = models.ForeignKey(Category)  # привязка к категории
    subcategory_name = models.CharField(max_length=256)


class TransactionType(models.Model):  # типы транзакций: 1 - income, 2 - outcome
    transaction_type = models.CharField(max_length=20)


class Transaction(models.Model):
    user = models.ForeignKey(User)
    billing = models.ForeignKey(Billing)
    transaction_type = models.ForeignKey(TransactionType)
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(Subcategory)
    datetime = models.DateTimeField()
    comment = models.TextField()