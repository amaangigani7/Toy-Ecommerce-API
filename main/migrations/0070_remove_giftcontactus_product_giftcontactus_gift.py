# Generated by Django 4.0.4 on 2022-06-13 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0069_alter_giftcontactus_message_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftcontactus',
            name='product',
        ),
        migrations.AddField(
            model_name='giftcontactus',
            name='gift',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.gift'),
        ),
    ]