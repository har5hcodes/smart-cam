# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from displaycode.models import Snippet,Comment, Camera, SnapshotDetails
admin.site.register(Snippet)
admin.site.register(Comment)
admin.site.register(Camera)
admin.site.register(SnapshotDetails)
