# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='contentType',
            field=models.CharField(default=b'text/plain', max_length=20, choices=[(b'text/x-markdown', b'Markdown'), (b'text/plain', b'Plain text')]),
        ),
    ]
