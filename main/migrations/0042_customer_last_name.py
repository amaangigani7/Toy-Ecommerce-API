# Generated by Django 4.0.4 on 2022-05-19 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_alter_shippingaddress_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
