# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='private',
        ),
        migrations.AddField(
            model_name='post',
            name='privacy',
            field=models.CharField(default=b'PB', max_length=4, choices=[(b'PV', b'Private to me'), (b'PA', b'Private to another author'), (b'PF', b'Private to my friends'), (b'FOAF', b'Friend of a friend'), (b'HF', b'Private to only friends on my host'), (b'PB', b'Public')]),
        ),
    ]
