# Generated by Django 2.2.4 on 2019-10-08 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20191008_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='available_package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=20)),
                ('amount', models.IntegerField()),
                ('queue_size', models.IntegerField()),
                ('account_connection_size', models.IntegerField()),
                ('team_member_size', models.IntegerField()),
                ('package_dirtybit', models.UUIDField(default=uuid.uuid4, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='current_package_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dirtybit', models.UUIDField(blank=True, null=True, unique=True)),
                ('queue_size', models.IntegerField(blank=True, null=True)),
                ('account_connection_size', models.IntegerField(blank=True, null=True)),
                ('team_member_size', models.IntegerField(blank=True, null=True)),
                ('package_selected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.available_package')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
