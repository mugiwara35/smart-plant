# Generated by Django 4.2.4 on 2023-08-16 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tanaman', '0014_jenis_tanaman_tanaman_jenis_tanaman'),
        ('panen', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PANEN',
            new_name='PREDIKSI_PANEN',
        ),
    ]
