# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_auto_20160330_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='imageFile',
            field=models.ImageField(default=b'images/None/no-img.jpg', upload_to=b''),
        ),
    ]
