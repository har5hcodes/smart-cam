# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-14 23:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('displaycode', '0005_comment_snippetid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='snippetId',
            field=models.IntegerField(),
        ),
    ]