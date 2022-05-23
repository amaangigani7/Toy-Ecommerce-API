# Generated by Django 4.0.4 on 2022-05-18 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_alter_gift_slug'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shippingaddress',
            unique_together={('customer', 'first_name', 'last_name', 'address_1', 'address_1', 'city', 'state', 'zipcode', 'country', 'phone_number')},
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='default_add',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]