# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0003_author_profile_pic'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GlobalAuthor',
        ),
        migrations.RemoveField(
            model_name='globalrelation',
            name='global_author',
        ),
        migrations.RemoveField(
            model_name='globalrelation',
            name='local_author',
        ),
        migrations.RemoveField(
            model_name='localrelation',
            name='author1',
        ),
        migrations.RemoveField(
            model_name='localrelation',
            name='author2',
        ),
        migrations.AddField(
            model_name='author',
            name='email',
            field=models.EmailField(default='null', max_length=80),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='GlobalRelation',
        ),
        migrations.DeleteModel(
            name='LocalRelation',
        ),
    ]
