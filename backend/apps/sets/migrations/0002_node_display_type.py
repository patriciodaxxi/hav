# Generated by Django 3.1.5 on 2021-01-15 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='display_type',
            field=models.CharField(blank=True, choices=[('', 'Default'), ('grouped_creation_day', 'Grouped by date'), ('grouped_title', 'Grouped by media title')], db_index=True, default='', max_length=20),
        ),
    ]
