# Generated by Django 3.1.1 on 2020-10-22 02:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0018_auto_20201022_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introcode',
            field=models.UUIDField(default=uuid.UUID('b5e963fd-003e-4e4b-aedf-06a04f581063')),
        ),
    ]
