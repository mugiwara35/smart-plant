# Generated by Django 4.2.4 on 2023-08-13 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tanaman', '0006_tanaman_min_kelembapan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tanaman',
            name='jadwal',
        ),
        migrations.RemoveField(
            model_name='tanaman',
            name='mode',
        ),
    ]
