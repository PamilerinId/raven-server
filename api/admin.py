# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Payee)
admin.site.register(Fee)
admin.site.register(CustomUser)
admin.site.register(Transaction)
