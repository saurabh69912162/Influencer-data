# Generated by Django 2.2.4 on 2019-10-20 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0043_temp_data_accs_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='temp_data',
            name='accs_provider',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
