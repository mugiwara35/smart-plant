# Generated by Django 4.2.4 on 2023-08-12 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tanaman', '0002_tanaman_tanggal_aktif_alter_tanaman_tanggal_menanam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tanaman',
            name='tanggal_menanam',
            field=models.DateField(blank=True, null=True),
        ),
    ]
