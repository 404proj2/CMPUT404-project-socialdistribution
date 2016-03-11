# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0002_globalauthor_globalrelation_localrelation'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_id', models.CharField(default=uuid.uuid4, unique=True, max_length=38)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('comment_text', models.TextField()),
                ('author', models.ForeignKey(to='authors.Author')),
                ('post', models.ForeignKey(to='posts.Post')),
            ],
        ),
    ]
