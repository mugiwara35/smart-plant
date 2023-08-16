from django.db import models
from tanaman.models import TANAMAN
# Create your models here.

class PANEN(models.Model):
    tanaman = models.ForeignKey(TANAMAN, on_delete=models.CASCADE, blank=True, null=True)
    suhu = models.IntegerField(blank=True, null=True)
    jumlah_air = models.IntegerField(blank=True, null=True)
    kelembapan = models.IntegerField(blank=True, null=True)
    status_panen = models.BooleanField(blank=True, null=True)
    
    def __str__(self):
        return "{}. {} : {}".format(self.id, self.tanaman, self.status_panen)