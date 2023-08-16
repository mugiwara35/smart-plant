from django.db import models

from alat.models import ALAT
from wadah_air.models import WADAH_AIR

# Create your models here.

class POMPA(models.Model):
    alat = models.ForeignKey(ALAT, on_delete=models.CASCADE, blank=True, null=True)
    wadah_air = models.ForeignKey(WADAH_AIR, on_delete=models.SET_NULL, blank=True, null=True)
    nama_pompa = models.CharField(max_length=40, blank=True, null=True)
    
    def __str__(self):
        return "{}. {} - {} - {}".format(self.id, self.alat.id, self.wadah_air.id, self.nama_pompa)