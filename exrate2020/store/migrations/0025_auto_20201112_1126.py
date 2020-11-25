# Generated by Django 3.1.1 on 2020-11-12 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_order_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='brand',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='model',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='package',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='series',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]