# Generated by Django 4.2.4 on 2023-08-14 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tanaman', '0007_remove_tanaman_jadwal_remove_tanaman_mode'),
    ]

    operations = [
        migrations.CreateModel(
            name='PENJADWALAN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu_menyiram', models.TimeField(blank=True, null=True)),
                ('lama_menyiram', models.IntegerField(blank=True, null=True)),
                ('tanaman', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tanaman.tanaman')),
            ],
        ),
    ]
