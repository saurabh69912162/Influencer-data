# Generated by Django 2.2.4 on 2019-10-16 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_auto_20191013_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='connections',
            name='account_token',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='upcomming_queue',
            name='timestamp',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
