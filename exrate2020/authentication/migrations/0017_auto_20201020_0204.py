# Generated by Django 3.1.1 on 2020-10-20 02:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_auto_20201017_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introcode',
            field=models.UUIDField(default=uuid.UUID('e7b2c9d6-4714-4da3-baea-491dd9b3f75f')),
        ),
    ]
