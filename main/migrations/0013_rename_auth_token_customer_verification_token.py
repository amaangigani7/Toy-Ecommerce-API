# Generated by Django 4.0.4 on 2022-05-14 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_customer_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='auth_token',
            new_name='verification_token',
        ),
    ]
