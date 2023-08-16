from django.urls import path
from . import views

urlpatterns = [
    path('', views.pompa_listView, name='pompa_list'),
    path('tambah/', views.pompa_tambahView, name='pompa_tambah'),
    path('tambah/berhasil/', views.berhasilView.as_view(aksi='pompa_tambah_berhasil'), name='pompa_tambah_berhasil'),
    path('ubah', views.pompa_ubahView, name='pompa_ubah'),
    path('ubah/berhasil/', views.berhasilView.as_view(aksi='pompa_ubah_berhasil'), name='pompa_ubah_berhasil'),
    path('hapus_berhasil/', views.berhasilView.as_view(aksi='pompa_hapus_berhasil'), name='pompa_hapus_berhasil'),
]