# Generated by Django 4.0.4 on 2022-05-15 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_shippingaddress_default_add'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='address',
            new_name='address_1',
        ),
        migrations.AlterUniqueTogether(
            name='shippingaddress',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='address_2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='state',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='zipcode',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='shippingaddress',
            unique_together={('customer', 'address_1', 'address_1', 'city', 'state', 'zipcode')},
        ),
    ]
