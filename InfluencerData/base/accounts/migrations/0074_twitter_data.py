# Generated by Django 2.2.4 on 2019-11-27 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0073_linkedin_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='twitter_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('screen_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('location', models.CharField(blank=True, max_length=1000, null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('website', models.CharField(blank=True, max_length=1000, null=True)),
                ('fan_count', models.BigIntegerField(blank=True, default=0, null=True)),
                ('friends_count', models.BigIntegerField(blank=True, default=0, null=True)),
                ('listed_count', models.BigIntegerField(blank=True, default=0, null=True)),
                ('created_at', models.CharField(blank=True, max_length=1000, null=True)),
                ('favourites_count', models.BigIntegerField(blank=True, default=0, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('profile_background_color', models.CharField(blank=True, max_length=1000, null=True)),
                ('profile_background_image_url_https', models.CharField(blank=True, max_length=1000, null=True)),
                ('profile_image_url_https', models.CharField(blank=True, max_length=1000, null=True)),
                ('profile_banner_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.selected_connections')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]