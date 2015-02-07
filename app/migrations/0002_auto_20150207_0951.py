# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='text',
        ),
        migrations.AddField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=160, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='url',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
    ]
