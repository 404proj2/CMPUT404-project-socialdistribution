# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0013_auto_20160319_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='url',
            field=models.URLField(default=b'https://mighty-cliffs-82717.herokuapp.com/author/'),
        ),
    ]
