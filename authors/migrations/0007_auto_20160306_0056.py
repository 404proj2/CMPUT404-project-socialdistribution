# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0006_auto_20160306_0045'),
    ]

    operations = [
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
        migrations.RenameField(
            model_name='globalauthor',
            old_name='host',
            new_name='url',
        ),
        migrations.RemoveField(
            model_name='author',
            name='friends',
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
