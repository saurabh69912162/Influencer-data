# Generated by Django 2.2.4 on 2019-10-08 03:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20191008_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='business_profile_data',
            name='dirtybit',
            field=models.UUIDField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='creator_profile_data',
            name='dirtybit',
            field=models.UUIDField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='business_profile_data',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='creator_profile_data',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]