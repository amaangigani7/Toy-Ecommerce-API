# Generated by Django 4.0.4 on 2022-05-25 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0051_rename_similarslug_similarproducts'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SimilarProducts',
            new_name='SimilarProduct',
        ),
    ]
