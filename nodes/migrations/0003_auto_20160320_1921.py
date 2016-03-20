# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0002_auto_20160320_1918'),
    ]

    operations = [
        migrations.RenameField(
            model_name='node',
            old_name='basic_pass',
            new_name='basic_auth_token',
        ),
        migrations.RemoveField(
            model_name='node',
            name='basic_user',
        ),
    ]
