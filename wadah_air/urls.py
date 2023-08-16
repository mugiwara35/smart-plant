from django.urls import path
from . import views

urlpatterns = [
    path('', views.wadah_listView, name='wadah_list'),
    path('tambah/', views.wadah_tambahView, name='wadah_tambah'),
    path('tambah/berhasil/', views.berhasilView.as_view(aksi='wadah_air_tambah_berhasil'), name='wadah_tambah_berhasil'),
    path('ubah', views.wadah_ubahView, name='wadah_ubah'),
    path('ubah/berhasil/', views.berhasilView.as_view(aksi='wadah_air_ubah_berhasil'), name='wadah_ubah_berhasil'),
    path('hapus_berhasil/', views.berhasilView.as_view(aksi='wadah_hapus_berhasil'), name='wadah_hapus_berhasil'),
]