# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_post_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='origin',
            field=models.URLField(default=b'https://mighty-cliffs-82717.herokuapp.com/', max_length=140),
        ),
        migrations.AlterField(
            model_name='post',
            name='source',
            field=models.URLField(default=b'https://mighty-cliffs-82717.herokuapp.com/', max_length=140),
        ),
    ]
