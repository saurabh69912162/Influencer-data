# Generated by Django 2.2.4 on 2019-11-20 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0055_auto_20191120_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_transaction',
            name='razorpay_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]