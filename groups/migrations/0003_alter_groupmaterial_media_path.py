# Generated by Django 4.2.13 on 2024-06-28 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("groups", "0002_alter_group_image_alter_group_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="groupmaterial",
            name="media_path",
            field=models.FileField(upload_to="groupMaterials/"),
        ),
    ]
