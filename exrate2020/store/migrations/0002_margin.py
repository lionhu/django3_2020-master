# Generated by Django 3.1.1 on 2020-10-05 03:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Margin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=1)),
                ('amount', models.IntegerField(default=0)),
                ('is_valid', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('paid_at', models.DateTimeField(auto_now=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='margins', to='store.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='margins', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]