# Generated by Django 2.2.4 on 2019-10-09 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20191009_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connections',
            name='dirtybit',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
