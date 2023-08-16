from django.db import models
from wadah_air.models import WADAH_AIR
from tanaman.models import TANAMAN
from alat.models import ALAT

# Create your models here.
class MONITORING(models.Model):
    tanaman = models.ForeignKey(TANAMAN, on_delete=models.SET_NULL, blank=True, null=True)
    kelembapan = models.IntegerField(blank=True, null=True)
    tingkat_air = models.IntegerField(blank=True, null=True)
    siram = models.BooleanField(blank=True, null=True, default=False)
    penggunaan_air = models.IntegerField(blank=True, null=True)
    waktu = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
            return "{}. {} - {}".format(self.id, self.tanaman, self.waktu)
    
