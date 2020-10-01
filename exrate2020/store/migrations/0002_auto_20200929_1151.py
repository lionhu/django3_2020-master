# Generated by Django 3.1.1 on 2020-09-29 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='inventory',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='is_valid',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
