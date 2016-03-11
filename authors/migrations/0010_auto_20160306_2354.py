# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0009_auto_20160306_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalrelation',
            name='global_author',
            field=models.ForeignKey(related_name='global_author', to='authors.GlobalAuthor'),
        ),
    ]
