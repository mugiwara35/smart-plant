from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.JENIS_TANAMAN)
admin.site.register(models.TANAMAN)
admin.site.register(models.PENJADWALAN)