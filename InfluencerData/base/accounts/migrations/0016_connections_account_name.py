# Generated by Django 2.2.4 on 2019-10-09 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20191009_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='connections',
            name='account_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]