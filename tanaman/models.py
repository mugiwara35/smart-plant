from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

from alat.models import ALAT
from pompa.models import POMPA
from akun.models import AKUN

PILIHAN_MODE = [
    ('lembab', 'Kelembapan'),
    ('jadwal', 'Jadwal'),
    
]

VALIDATOR_JAM = [
    MinValueValidator(1),
    MaxValueValidator(24),
]

VALIDATOR_MENIT = [
    MinValueValidator(0),
    MaxValueValidator(59),
]

class JENIS_TANAMAN(models.Model):
    nama_jenis = models.CharField(max_length=40, blank=True, null=True)
    waktu_panen = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return "{}. {}".format(self.id, self.nama_jenis)

class TANAMAN(models.Model):
    akun = models.ForeignKey(AKUN, on_delete=models.CASCADE, blank=True, null=True)
    jenis_tanaman = models.ForeignKey(JENIS_TANAMAN, on_delete=models.SET_NULL, blank=True, null=True)
    pompa = models.ForeignKey(POMPA, on_delete=models.SET_NULL, blank=True, null=True)
    nama_tanaman = models.CharField(max_length=40, blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)
    min_kelembapan = models.IntegerField(blank=True, null=True)
    mode = models.CharField(max_length=6,choices=PILIHAN_MODE, null=True, default='')
    tanggal_menanam = models.DateField(blank=True, null=True)
    tanggal_aktif = models.DateTimeField(blank=True, null=True, default=now)
    
    def __str__(self):
        return "{}. {} - {}".format(self.id, self.pompa, self.nama_tanaman)
    
class PENJADWALAN(models.Model):
    akun = models.ForeignKey(AKUN, on_delete=models.CASCADE, blank=True, null=True)
    tanaman = models.ForeignKey(TANAMAN, on_delete=models.CASCADE, blank=True, null=True)
    waktu_menyiram = models.TimeField(blank=True, null=True)
    jam = models.IntegerField(validators=VALIDATOR_JAM, blank=True, null=True)
    menit = models.IntegerField(validators=VALIDATOR_MENIT, blank=True, null=True)
    lama_menyiram = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return "{}. {} - {}.{}".format(self.id, self.tanaman, self.jam, self.menit)
    
