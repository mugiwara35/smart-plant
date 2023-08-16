from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AKUN(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nama = models.CharField(max_length=60, blank=True, null=True)
    
    def __str__(self):
        return "{}. {} - {}".format(self.id, self.user.username, self.nama)
    
