# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-14 21:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsevents', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='country',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
