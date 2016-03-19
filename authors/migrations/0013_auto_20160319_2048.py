# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0012_auto_20160311_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='url',
            field=models.URLField(default=b'https://mighty-cliffs-82717.herokuapp.com/author/<function uuid4 at 0x7f472ad407d0>'),
        ),
    ]
