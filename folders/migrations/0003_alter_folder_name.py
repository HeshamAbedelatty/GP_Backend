# Generated by Django 4.2.13 on 2024-07-02 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("folders", "0002_remove_file_name_alter_folder_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="folder",
            name="name",
            field=models.CharField(max_length=255),
        ),
    ]
