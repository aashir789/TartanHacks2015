# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150207_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='Bus',
            field=models.CharField(max_length=160, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='Direction',
            field=models.CharField(max_length=160, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='stopname',
            field=models.CharField(max_length=160, blank=True),
            preserve_default=True,
        ),
    ]
