# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.utils import timezone
from .consts import *


class User(AbstractBaseUser):
    username = models.CharField(max_length=256, unique=True)
    email = models.CharField(max_length=256)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    birth_date = models.DateField(default='1900-01-01')

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'email']


class Currency(models.Model):
    currency = models.SmallIntegerField(choices=CURRENCY_CHOICES)


class BillingTypes(models.Model):
    billing_type = models.SmallIntegerField(choices=BILLING_TYPE_CHOICES)


class Billing(models.Model):
    user = models.ForeignKey(User)
    billing_name = models.CharField(max_length=256)
    billing_type = models.ForeignKey(BillingTypes)
    currency = models.ForeignKey(Currency)
    money = models.FloatField(default=0)


class CategoryTypes(models.Model):
    category_type = models.SmallIntegerField(choices=CATEGORY_TYPE_CHOICES)


class Category(models.Model):
    category_name = models.CharField(max_length=256)
    user = models.ForeignKey(User)
    category_type = models.ForeignKey(CategoryTypes)


class Subcategory(models.Model):
    category = models.ForeignKey(Category)
    subcategory_name = models.CharField(max_length=256)


class TransactionType(models.Model):
    transaction_type = models.SmallIntegerField(choices=TRANSACTION_TYPE_CHOICES)


class Transaction(models.Model):
    user = models.ForeignKey(User)
    billing = models.ForeignKey(Billing)
    transaction_type = models.ForeignKey(TransactionType)
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(Subcategory)
    money = models.FloatField(default=0)
    datetime = models.DateTimeField()
    comment = models.TextField()