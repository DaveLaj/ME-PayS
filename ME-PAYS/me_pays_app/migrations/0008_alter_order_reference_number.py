# Generated by Django 4.2 on 2023-06-18 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('me_pays_app', '0007_remove_order_school_id_order_enduser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='reference_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
