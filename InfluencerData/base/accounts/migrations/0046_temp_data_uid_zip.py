# Generated by Django 2.2.4 on 2019-10-20 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0045_auto_20191020_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='temp_data',
            name='uid_zip',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
    ]