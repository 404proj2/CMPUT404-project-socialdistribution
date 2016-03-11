# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0005_auto_20160306_0039'),
    ]

    operations = [
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
        migrations.RemoveField(
            model_name='globalauthor',
            name='url',
        ),
        migrations.AddField(
            model_name='author',
            name='friends',
            field=models.ManyToManyField(related_name='friends', null=True, to='authors.GlobalAuthor', blank=True),
        ),
        migrations.AddField(
            model_name='globalauthor',
            name='host',
            field=models.URLField(default=b'http://127.0.0.1:8000/', blank=True),
        ),
        migrations.DeleteModel(
            name='GlobalRelation',
        ),
        migrations.DeleteModel(
            name='LocalRelation',
        ),
    ]
