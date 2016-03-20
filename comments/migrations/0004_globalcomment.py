# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0012_auto_20160311_2332'),
        ('posts', '0009_auto_20160312_0215'),
        ('comments', '0003_auto_20160312_0215'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment_id', models.CharField(default=uuid.uuid4, unique=True, max_length=38)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date published')),
                ('comment_text', models.TextField()),
                ('contentType', models.CharField(default=b'text/plain', max_length=20, choices=[(b'text/x-markdown', b'Markdown'), (b'text/plain', b'Plain text')])),
                ('author', models.ForeignKey(to='authors.GlobalAuthor')),
                ('post', models.ForeignKey(to='posts.Post')),
            ],
        ),
    ]
