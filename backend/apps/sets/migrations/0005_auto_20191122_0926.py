# Generated by Django 2.2.4 on 2019-11-22 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("sets", "0004_node_tags")]

    operations = [
        migrations.AlterField(
            model_name="node",
            name="tags",
            field=models.ManyToManyField(blank=True, to="tags.Tag"),
        )
    ]
