# Generated by Django 4.2.4 on 2023-08-14 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tanaman', '0010_alter_tanaman_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tanaman',
            name='mode',
            field=models.CharField(choices=[('lembab', 'Kelembapan'), ('jadwal', 'Jadwal')], default='', max_length=6, null=True),
        ),
    ]