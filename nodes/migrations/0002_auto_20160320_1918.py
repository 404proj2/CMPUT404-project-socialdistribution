# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='basic_pass',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='node',
            name='basic_user',
            field=models.TextField(default=b''),
        ),
    ]
