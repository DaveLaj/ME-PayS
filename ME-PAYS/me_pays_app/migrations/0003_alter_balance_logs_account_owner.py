# Generated by Django 4.2 on 2023-06-25 03:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('me_pays_app', '0002_initialize_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance_logs',
            name='account_Owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_balance_logs', to=settings.AUTH_USER_MODEL),
        ),
    ]
