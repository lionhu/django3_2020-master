# Generated by Django 3.1.1 on 2020-09-24 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studydjango', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='schoole',
            new_name='school',
        ),
    ]
