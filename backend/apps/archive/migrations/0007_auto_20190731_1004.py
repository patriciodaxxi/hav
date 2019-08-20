# Generated by Django 2.2.3 on 2019-07-31 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0014_mediacreator_email'),
        ('archive', '0006_auto_20190327_2049'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileCreator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media.MediaCreator')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.ArchiveFile')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='media.MediaCreatorRole')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='archivefile',
            name='creators',
            field=models.ManyToManyField(through='archive.FileCreator', to='media.MediaCreator', verbose_name='creators'),
        ),
    ]