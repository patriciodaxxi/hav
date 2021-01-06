# Generated by Django 3.1.3 on 2021-01-06 20:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('media', '0001_initial'),
        ('tags', '0001_initial'),
        ('hav_collections', '0002_collection_root_node'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sets', '0001_initial'),
        ('archive', '0002_auto_20210106_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='attachments',
            field=models.ManyToManyField(blank=True, related_name='is_attachment_for', to='archive.AttachmentFile'),
        ),
        migrations.AddField(
            model_name='media',
            name='collection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='hav_collections.collection'),
        ),
        migrations.AddField(
            model_name='media',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_media', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='media',
            name='creators',
            field=models.ManyToManyField(through='media.MediaToCreator', to='media.MediaCreator', verbose_name='creators'),
        ),
        migrations.AddField(
            model_name='media',
            name='files',
            field=models.ManyToManyField(to='archive.ArchiveFile'),
        ),
        migrations.AddField(
            model_name='media',
            name='license',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='media.license'),
        ),
        migrations.AddField(
            model_name='media',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modified_media', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='media',
            name='original_media_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='media.mediatype'),
        ),
        migrations.AddField(
            model_name='media',
            name='set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sets.node'),
        ),
        migrations.AddField(
            model_name='media',
            name='tags',
            field=models.ManyToManyField(to='tags.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='mediatocreator',
            unique_together={('creator', 'role', 'media')},
        ),
    ]
