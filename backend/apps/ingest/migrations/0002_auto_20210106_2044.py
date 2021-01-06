# Generated by Django 3.1.3 on 2021-01-06 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('media', '0001_initial'),
        ('ingest', '0001_initial'),
        ('sets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingestqueue',
            name='created_media_entries',
            field=models.ManyToManyField(blank=True, editable=False, to='media.Media'),
        ),
        migrations.AddField(
            model_name='ingestqueue',
            name='target',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sets.node'),
        ),
    ]
