# Generated by Django 2.2.4 on 2019-11-20 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0051_queue_statistics_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='available_package',
            name='package_id_int',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
