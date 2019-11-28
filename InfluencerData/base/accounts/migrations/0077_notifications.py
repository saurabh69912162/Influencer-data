# Generated by Django 2.2.4 on 2019-11-28 11:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0076_auto_20191128_0924'),
    ]

    operations = [
        migrations.CreateModel(
            name='notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(max_length=1000)),
                ('message', models.CharField(max_length=1000)),
                ('sender_url', models.URLField()),
                ('notification_type', models.IntegerField()),
                ('datetime', models.DateTimeField()),
                ('read', models.BooleanField(default=False)),
                ('mark_as_read_all', models.BooleanField(default=False)),
                ('read_datetime', models.DateTimeField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
