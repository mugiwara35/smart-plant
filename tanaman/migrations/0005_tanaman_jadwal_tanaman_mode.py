# Generated by Django 4.2.4 on 2023-08-13 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tanaman', '0004_remove_tanaman_alat_tanaman_pompa'),
    ]

    operations = [
        migrations.AddField(
            model_name='tanaman',
            name='jadwal',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tanaman',
            name='mode',
            field=models.CharField(blank=True, choices=[('jadwal', 'Jadwal'), ('kering', 'Kering')], max_length=6, null=True),
        ),
    ]
