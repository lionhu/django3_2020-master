# Generated by Django 3.1.1 on 2020-11-04 22:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0024_auto_20201104_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='introcode',
            field=models.UUIDField(default=uuid.UUID('aab043bf-46f9-454c-a928-bd9541741278')),
        ),
    ]