# Generated by Django 4.0.4 on 2022-05-25 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0050_similarslug'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SimilarSlug',
            new_name='SimilarProducts',
        ),
    ]