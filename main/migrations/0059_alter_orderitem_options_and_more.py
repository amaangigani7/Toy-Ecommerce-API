# Generated by Django 4.0.4 on 2022-06-09 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0058_gift_in_stock_gift_mega_menu_gift_meta_description_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['-placed_on']},
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='date_added',
            new_name='placed_on',
        ),
    ]
