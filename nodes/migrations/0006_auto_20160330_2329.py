# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0005_node_allow_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='basic_auth_password',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='node',
            name='basic_auth_username',
            field=models.TextField(default=b''),
        ),
    ]
