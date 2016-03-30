# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='post',
            field=models.ForeignKey(default=None, to='posts.Post'),
        ),
        migrations.AlterField(
            model_name='image',
            name='imageFile',
            field=models.FileField(default=b'images/None/no-img.jpg', upload_to=b'images/'),
        ),
    ]
