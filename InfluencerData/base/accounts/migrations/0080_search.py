# Generated by Django 2.2.4 on 2019-11-28 13:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0079_delete_notification_pannel'),
    ]

    operations = [
        migrations.CreateModel(
            name='search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('location', models.CharField(max_length=100)),
                ('platform', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(max_length=100)),
                ('reach', models.BigIntegerField(blank=True, null=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
