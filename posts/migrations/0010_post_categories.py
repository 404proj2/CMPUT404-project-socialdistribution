# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20160312_0215'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.CharField(max_length=64, blank=True),
        ),
    ]
