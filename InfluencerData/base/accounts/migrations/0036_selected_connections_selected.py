# Generated by Django 2.2.4 on 2019-10-18 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_auto_20191017_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='selected_connections',
            name='selected',
            field=models.BooleanField(default=False),
        ),
    ]
