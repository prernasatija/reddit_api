# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-21 03:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20171221_0351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='article',
            new_name='reddit_id',
        ),
    ]
