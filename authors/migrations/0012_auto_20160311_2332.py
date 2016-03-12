# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0011_author_github'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='host',
            field=models.CharField(default=b'https://mighty-cliffs-82717.herokuapp.com/', max_length=100),
        ),
        migrations.AlterField(
            model_name='globalauthor',
            name='host',
            field=models.CharField(default=b'https://mighty-cliffs-82717.herokuapp.com/', max_length=100),
        ),
    ]
