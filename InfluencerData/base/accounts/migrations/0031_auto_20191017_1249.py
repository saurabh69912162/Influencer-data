# Generated by Django 2.2.4 on 2019-10-17 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_queue_statistics_user_connection_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_connection_data',
            name='max_connections',
            field=models.IntegerField(default=8),
        ),
        migrations.AlterField(
            model_name='user_connection_data',
            name='max_seleceted_connections',
            field=models.IntegerField(default=8),
        ),
    ]
