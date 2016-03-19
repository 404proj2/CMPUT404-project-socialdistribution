# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('node_id', models.CharField(default=uuid.uuid4, unique=True, max_length=38)),
                ('add_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date added')),
                ('node_name', models.TextField()),
                ('node_url', models.TextField()),
            ],
        ),
    ]
