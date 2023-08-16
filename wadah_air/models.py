from django.db import models
from akun.models import AKUN

# Create your models here.

class WADAH_AIR(models.Model):
    akun = models.ForeignKey(AKUN, on_delete=models.SET_NULL, blank=True, null=True)
    nama_wadah = models.CharField(max_length=40, blank=True, null=True)
    maks_liter = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return "{}. {}".format(self.id, self.nama_wadah)