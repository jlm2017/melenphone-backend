# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callcenter', '0007_achievement_phi'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='codeName',
            field=models.CharField(default='None', max_length=50),
        ),
    ]
