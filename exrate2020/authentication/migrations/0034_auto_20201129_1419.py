# Generated by Django 3.1.1 on 2020-11-29 14:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0033_auto_20201129_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introcode',
            field=models.UUIDField(default=uuid.UUID('6c577df6-df49-4232-8afe-96c279bf551e')),
        ),
    ]
