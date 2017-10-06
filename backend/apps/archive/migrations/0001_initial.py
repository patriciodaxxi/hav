# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-05 12:16
from __future__ import unicode_literals

import apps.archive.storage
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(editable=False, storage=apps.archive.storage.ArchiveStorage, upload_to='')),
                ('original_filename', models.CharField(blank=True, editable=False, max_length=200)),
                ('source_id', models.CharField(blank=True, max_length=200)),
                ('hash', models.CharField(db_index=True, max_length=40, unique=True)),
                ('archived_at', models.DateTimeField(auto_now_add=True)),
                ('archived_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
