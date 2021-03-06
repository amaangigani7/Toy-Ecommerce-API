# Generated by Django 4.0.4 on 2022-06-13 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0071_alter_giftcontactus_message_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-id']},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='transaction_id',
            new_name='order_id',
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='signature',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together={('customer', 'payment_id')},
        ),
    ]
