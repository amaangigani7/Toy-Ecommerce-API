# Generated by Django 4.0.4 on 2022-06-23 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0075_rename_amount_paid_order_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='amount',
        ),
    ]
