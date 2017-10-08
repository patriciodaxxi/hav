# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-08 08:27
from __future__ import unicode_literals

import apps.archive.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0002_archivefile_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivefile',
            name='file',
            field=models.FileField(editable=False, storage=apps.archive.storage.ArchiveStorage(), upload_to='%Y/%m/%d'),
        ),
    ]
