# Generated by Django 2.2.4 on 2019-10-20 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0044_temp_data_accs_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduler_model',
            name='scheduled_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
