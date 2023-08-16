from django.urls import path
from . import views

urlpatterns = [
    path('', views.tanaman_listView, name='tanaman_list'),
    path('tambah/', views.tanaman_tambahView, name='tanaman_tambah'),
    path('tambah/berhasil/', views.berhasilView.as_view(aksi='tanaman_tambah_berhasil'), name='tanaman_tambah_berhasil'),
    path('ubah', views.tanaman_ubahView, name='tanaman_ubah'),
    path('ubah/berhasil/', views.berhasilView.as_view(aksi='tanaman_ubah_berhasil'), name='tanaman_ubah_berhasil'),
    path('hapus_berhasil/', views.berhasilView.as_view(aksi='tanaman_hapus_berhasil'), name='tanaman_hapus_berhasil'),
    
]