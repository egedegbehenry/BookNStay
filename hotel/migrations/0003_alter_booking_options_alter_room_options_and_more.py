# Generated by Django 5.0.6 on 2024-07-03 22:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_alter_room_category_booking'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ['-created_at'], 'verbose_name': 'Booking', 'verbose_name_plural': 'Bookings'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['number'], 'verbose_name': 'Room', 'verbose_name_plural': 'Rooms'},
        ),
        migrations.AddField(
            model_name='booking',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='booking',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='room',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='room',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='beds',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='room',
            name='capacity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='room',
            name='category',
            field=models.CharField(choices=[('DEL', 'Deluxe'), ('KIN', 'King'), ('QUE', 'Queen'), ('STE', 'Suite'), ('EXE', 'Executive'), ('SIN', 'Single')], max_length=3),
        ),
        migrations.AlterField(
            model_name='room',
            name='number',
            field=models.PositiveIntegerField(),
        ),
    ]
