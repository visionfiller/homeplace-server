# Generated by Django 4.2.1 on 2023-06-06 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeplaceapi', '0003_remove_reservation_payment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='swapper',
            name='properties',
            field=models.ManyToManyField(related_name='swapper_properties', to='homeplaceapi.property'),
        ),
    ]
