# Generated by Django 4.0.4 on 2022-06-13 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0065_alter_shippingaddress_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shippingaddress',
            unique_together={('customer', 'address_1', 'address_1')},
        ),
    ]
