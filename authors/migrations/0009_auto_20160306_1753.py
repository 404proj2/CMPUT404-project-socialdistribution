# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0008_auto_20160306_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalrelation',
            name='relation_status',
            field=models.CharField(default=0, max_length=9, choices=[(0, b'FOLLOWS'), (1, b'FOLLOWED'), (2, b'FRIENDS')]),
        ),
    ]
