# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0010_auto_20160306_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='github',
            field=models.URLField(blank=True),
        ),
    ]
