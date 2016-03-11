# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0002_globalauthor_globalrelation_localrelation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_id', models.CharField(default=uuid.uuid4, unique=True, max_length=38)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('post_text', models.TextField()),
                ('post_title', models.CharField(max_length=64)),
                ('post_type', models.CharField(default=b'PT', max_length=2, choices=[(b'MD', b'Markdown'), (b'PT', b'Plain text')])),
                ('private', models.BooleanField(default=b'True')),
                ('author', models.ForeignKey(to='authors.Author')),
            ],
        ),
    ]
