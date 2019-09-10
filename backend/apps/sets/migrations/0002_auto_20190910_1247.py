# Generated by Django 2.2.4 on 2019-09-10 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
        ('sets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='node',
            name='tags',
            field=models.ManyToManyField(blank=True, to='tags.Tag'),
        ),
    ]
