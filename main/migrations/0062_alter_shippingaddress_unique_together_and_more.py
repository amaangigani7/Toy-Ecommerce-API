# Generated by Django 4.0.4 on 2022-06-13 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0061_order_coupon_used'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shippingaddress',
            unique_together={('customer', 'address_1', 'address_1', 'city', 'state', 'zipcode', 'country')},
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='phone_number',
        ),
    ]
