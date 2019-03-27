# Generated by Django 2.1.7 on 2019-03-27 20:29

from django.db import migrations


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# apps.media.migrations.0012_auto_20190327_2009

def move_source(apps, schema_editor):
    Media = apps.get_model('media', 'Media')
    ArchiveFile = apps.get_model('archive', 'ArchiveFile')
    for media in Media.objects.all():
        try:
            file = ArchiveFile.objects.filter(media__pk=media.pk).order_by('archived_at').first()
        except ArchiveFile.DoesNotExist:
            continue
        else:
            file.source_id = media.source
            file.save()

class Migration(migrations.Migration):


    dependencies = [
        ('media', '0011_media_attachments'),
    ]

    operations = [
        migrations.RunPython(
            code=move_source,
        ),
        migrations.RemoveField(
            model_name='media',
            name='source',
        ),
    ]
