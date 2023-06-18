# Generated by Django 4.2 on 2023-06-18 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('me_pays_app', '0006_order_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='school_id',
        ),
        migrations.AddField(
            model_name='order',
            name='enduser',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='me_pays_app.enduser'),
        ),
    ]
