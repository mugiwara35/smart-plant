from django.urls import path
from . import views

urlpatterns = [
    path('prediksi_panen', views.prediksi_panenView, name='prediksi_panen'),
    path('prediksi_panen/berhasil_panen', views.klasifikasiView.as_view(aksi='klasifikasi_panen_berhasil'), name='klasifikasi_berhasil'),
    path('prediksi_panen/gagal_panen', views.klasifikasiView.as_view(aksi='klasifikasi_panen_gagal'), name='klasifikasi_gagal'),
    path('test_keberhasilan', views.test_panenView, name='test_panen'),
    path('hasil_panen', views.hasil_panen_listView, name='hasil_panen_list'),
    path('hasil_panen/tambah', views.hasil_panen_tambahView, name='hasil_panen_tambah'),
    path('hasil_panen/ubah', views.hasil_panen_ubahView, name='hasil_panen_ubah'),
    path('hasil_panen/tambah/berhasil', views.berhasilView.as_view(aksi='hasil_panen_tambah_berhasil'), name='hasil_panen_tambah_berhasil'),
    path('hasil_panen/ubah/berhasil', views.berhasilView.as_view(aksi='hasil_panen_ubah_berhasil'), name='hasil_panen_ubah_berhasil'),
    path('hasil_panen/hapus_berhasil', views.berhasilView.as_view(aksi='hasil_panen_hapus_berhasil'), name='hasil_panen_hapus_berhasil'),
    
    
    
    
]