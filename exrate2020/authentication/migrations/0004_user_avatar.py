# Generated by Django 3.1.1 on 2020-09-15 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20200914_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
