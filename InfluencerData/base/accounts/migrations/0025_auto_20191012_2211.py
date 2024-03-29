# Generated by Django 2.2.4 on 2019-10-12 22:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_scheduler_model_hit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scheduler_model',
            name='status',
        ),
        migrations.CreateModel(
            name='upcomming_queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dirtybit', models.UUIDField(blank=True, null=True)),
                ('timestamp', models.CharField(blank=True, max_length=20, null=True)),
                ('init_schedule_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.init_schedule')),
                ('schedule_dirtybit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.scheduler_model')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
