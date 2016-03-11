# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20160309_0124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='id',
        ),
        migrations.AlterField(
            model_name='post',
            name='post_id',
            field=models.CharField(default=uuid.uuid4, max_length=38, unique=True, serialize=False, primary_key=True),
        ),
    ]
