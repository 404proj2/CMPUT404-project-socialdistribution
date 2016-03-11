# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0004_auto_20160305_2353'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('global_author_id', models.CharField(default=uuid.uuid4, unique=True, max_length=38)),
                ('global_author_name', models.CharField(max_length=50)),
                ('url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relation_status', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='LocalRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relation_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='author',
            name='email',
        ),
        migrations.AddField(
            model_name='localrelation',
            name='author1',
            field=models.ForeignKey(related_name='author1', to='authors.Author'),
        ),
        migrations.AddField(
            model_name='localrelation',
            name='author2',
            field=models.ForeignKey(related_name='author2', to='authors.Author'),
        ),
        migrations.AddField(
            model_name='globalrelation',
            name='global_author',
            field=models.ForeignKey(related_name='global_author', to='authors.Author'),
        ),
        migrations.AddField(
            model_name='globalrelation',
            name='local_author',
            field=models.ForeignKey(related_name='local_author', to='authors.Author'),
        ),
    ]
