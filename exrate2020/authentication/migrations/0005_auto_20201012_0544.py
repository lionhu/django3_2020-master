# Generated by Django 3.1.1 on 2020-10-12 05:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20201012_0507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introcode',
            field=models.UUIDField(default=uuid.UUID('d9e41981-d819-4ce7-be2f-5b72e6028161')),
        ),
    ]
