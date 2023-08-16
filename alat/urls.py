from django.urls import path
from . import views

urlpatterns = [
    path('', views.alat_listView, name='alat_list'),
    path('tambah/', views.alat_tambahView, name='alat_tambah'),
    path('tambah/berhasil/', views.berhasilView.as_view(aksi='alat_tambah_berhasil'), name='alat_tambah_berhasil'),
    path('ubah/', views.alat_ubahView, name='alat_ubah'),
    path('ubah/berhasil/', views.berhasilView.as_view(aksi='alat_ubah_berhasil'), name='alat_ubah_berhasil'),
    path('hapus_berhasil/', views.berhasilView.as_view(aksi='alat_hapus_berhasil'), name='alat_hapus_berhasil'),
    
]