# Generated by Django 2.2.4 on 2019-10-20 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0042_auto_20191019_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='temp_data',
            name='accs_name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
