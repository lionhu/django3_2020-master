# Generated by Django 3.1.1 on 2020-10-12 06:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_auto_20201012_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introcode',
            field=models.UUIDField(default=uuid.UUID('841f0cae-abb9-4ae6-9450-1616d55ac7ed')),
        ),
    ]
