# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0004_node_node_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='allow_access',
            field=models.BooleanField(default=False),
        ),
    ]
