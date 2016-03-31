# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nodes', '0003_auto_20160320_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='node_user',
            field=models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
