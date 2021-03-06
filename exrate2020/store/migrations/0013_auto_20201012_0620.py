# Generated by Django 3.1.1 on 2020-10-12 06:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20201012_0619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('f4a5a90b-32fa-42b5-ae98-0cf7ad379fda'), editable=False),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='store.order'),
        ),
    ]
