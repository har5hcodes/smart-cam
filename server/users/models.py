# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        SEPERATOR = "~"
        result = None
        if (self.email is not None):
            result = self.email
        if (self.username is not None):
            result = result + SEPERATOR + self.username
        return result
