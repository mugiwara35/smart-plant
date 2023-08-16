from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from akun.models import AKUN
# Create your models here.

class ALAT(models.Model):
    akun = models.ForeignKey(AKUN, on_delete=models.SET_NULL, blank=True, null=True)
    nama_alat = models.CharField(max_length=40, blank=True, null=True)
    mac_esp = models.CharField(max_length=20, blank=True, null=True)
    ssid = models.CharField(max_length=40, blank=True, null=True)
    tanggal_aktif = models.DateTimeField(blank=True, null=True, default=now)
    
    def __str__(self):
        return "{}. {} - {}".format(self.id, self.akun, self.nama_alat)