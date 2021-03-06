# Generated by Django 4.0.4 on 2022-05-25 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0053_specialproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('by', models.CharField(max_length=255)),
                ('review', models.TextField()),
                ('rating', models.IntegerField()),
                ('img_link', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='MakerClassReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('by', models.CharField(max_length=255)),
                ('review', models.TextField()),
                ('rating', models.IntegerField()),
                ('img_link', models.CharField(max_length=2000)),
                ('type', models.CharField(choices=[('Schools', 'Schools'), ('NGOs', 'NGOs'), ('Hobby Centers', 'Hobby Centers'), ('Clubs', 'Clubs')], max_length=255)),
            ],
        ),
    ]
