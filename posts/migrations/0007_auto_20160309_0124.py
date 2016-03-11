# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20160308_2353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='post_text',
            new_name='content',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='pub_date',
            new_name='published',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='post_title',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='post',
            name='post_type',
        ),
        migrations.RemoveField(
            model_name='post',
            name='privacy',
        ),
        migrations.AddField(
            model_name='post',
            name='contentType',
            field=models.CharField(default=b'text/plain', max_length=20, choices=[(b'text/x-markdown', b'Markdown'), (b'text/plain', b'Plain text')]),
        ),
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=140, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='origin',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='source',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='visibility',
            field=models.CharField(default=b'PUBLIC', max_length=10, choices=[(b'PRIVATE', b'Private to me'), (b'AUTHOR', b'Private to another author'), (b'FRIENDS', b'Private to my friends'), (b'FOAF', b'Friend of a friend'), (b'SERVERONLY', b'Private to only friends on my host'), (b'PUBLIC', b'Public')]),
        ),
    ]
