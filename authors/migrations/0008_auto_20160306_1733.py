# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0007_auto_20160306_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='host',
            field=models.CharField(default=b'http://127.0.0.1:8000/', max_length=100),
        ),
        migrations.AddField(
            model_name='globalauthor',
            name='host',
            field=models.CharField(default=b'http://127.0.0.1:8000/', max_length=100),
        ),
        migrations.AlterField(
            model_name='globalauthor',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
