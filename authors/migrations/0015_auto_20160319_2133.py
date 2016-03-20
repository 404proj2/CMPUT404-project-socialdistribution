# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0014_auto_20160319_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
