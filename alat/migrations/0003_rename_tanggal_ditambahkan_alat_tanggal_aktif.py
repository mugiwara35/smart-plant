# Generated by Django 4.2.4 on 2023-08-10 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alat', '0002_alat_tanggal_ditambahkan'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alat',
            old_name='tanggal_ditambahkan',
            new_name='tanggal_aktif',
        ),
    ]
