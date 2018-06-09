# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Payee(models.Model):
    name = models.CharField(max_length=256)
    email = models.EmailField()
    address = models.CharField(max_length=256)

    def __str__(self):
        return str(self.name)


class CustomUser(AbstractUser):
    school_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True, null=True)
    logo = models.ImageField(upload_to="uploads", max_length=100)
    description = models.TextField(max_length=None)
    address = models.TextField(max_length=512)
    tel = models.CharField(max_length=15)
    region = models.CharField(max_length=256)
    approval = models.CharField(max_length=256)
    bvn = models.CharField(max_length=15)
    account_number = models.CharField(max_length=20)

    def __str__(self):
        return str(self.school_name)


class Fee(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    amount = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return str(self.name)


class Transaction(models.Model):
    paid_to = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    received_from = models.ForeignKey(Payee)
    fee = models.ForeignKey(Fee)
    comments = models.TextField()
    pay_date = models.DateTimeField(auto_now=False)








