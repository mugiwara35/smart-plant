from django.db import models
from tanaman.models import TANAMAN
# Create your models here.

class HASIL_PANEN(models.Model):
    tanaman = models.ForeignKey(TANAMAN, on_delete=models.CASCADE, blank=True, null=True)
    jumlah_buah = models.IntegerField(blank=True, null=True)
    tanggal_panen = models.DateField(blank=True, null=True)

    def __str__(self):
        return "{}. {} : {}".format(self.id, self.tanaman, self.status_panen)

class PREDIKSI_PANEN(models.Model):
    tanaman = models.ForeignKey(TANAMAN, on_delete=models.CASCADE, blank=True, null=True)
    suhu = models.IntegerField(blank=True, null=True)
    jumlah_air = models.IntegerField(blank=True, null=True)
    kelembapan = models.IntegerField(blank=True, null=True)
    status_panen = models.BooleanField(blank=True, null=True)
    
    def __str__(self):
        return "{}. {} : {}".format(self.id, self.tanaman, self.status_panen)